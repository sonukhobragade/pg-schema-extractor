"""
Table extractor for PostgreSQL database.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any

from src.extractors.base_extractor import BaseExtractor
from src.models.database_objects import Table, Column


class TableExtractor(BaseExtractor):
    """
    Extractor for PostgreSQL tables and their columns.
    """
    
    def extract(self) -> Dict[str, Table]:
        """
        Extract tables from the database.
        
        Returns:
            Dict[str, Table]: Dictionary of tables by qualified name
        """
        self.logger.info("Extracting tables from database")
        tables = {}
        
        # Get tables
        table_query = """
            SELECT 
                t.oid,
                n.nspname AS schema,
                t.relname AS name,
                u.rolname AS owner,
                obj_description(t.oid, 'pg_class') AS comment,
                t.reltuples::bigint AS estimated_row_count,
                pg_total_relation_size(t.oid) AS total_size_bytes,
                t.relkind = 'p' AS is_partitioned,
                pg_stat_get_last_analyze_time(t.oid) AS last_analyzed,
                t.relhassubclass AS has_inheritance,
                -- PostgreSQL does not record table creation time: pg_class has
                -- no relcreated column, and selecting it made every extraction
                -- fail before returning a row. The closest available signal is
                -- the last time the planner saw the table.
                NULL::timestamptz AS created_at,
                GREATEST(pg_stat_get_last_autoanalyze_time(t.oid),
                         pg_stat_get_last_analyze_time(t.oid)) AS modified_at
            FROM 
                pg_class t
                JOIN pg_namespace n ON n.oid = t.relnamespace
                JOIN pg_roles u ON u.oid = t.relowner
            WHERE 
                t.relkind IN ('r', 'p')
                AND n.nspname NOT IN %(exclude_schemas)s
            ORDER BY 
                n.nspname, t.relname
        """
        
        table_results = self.execute_query(
            table_query, 
            {"exclude_schemas": tuple(self.exclude_schemas)}
        )
        
        for table_data in table_results:
            schema = table_data["schema"]
            name = table_data["name"]
            
            if not self.should_include_object(schema, name):
                continue
                
            qualified_name = f"{schema}.{name}"
            
            # Extract columns for this table
            columns = self._extract_columns(table_data["oid"])
            
            # Extract primary key
            primary_key = self._extract_primary_key(table_data["oid"])
            
            # Extract foreign keys
            foreign_keys = self._extract_foreign_keys(table_data["oid"])
            
            # Extract unique constraints
            unique_constraints = self._extract_unique_constraints(table_data["oid"])
            
            # Extract check constraints
            check_constraints = self._extract_check_constraints(table_data["oid"])
            
            # Extract indexes
            indexes = self._extract_indexes(table_data["oid"])
            
            # Extract partition info if applicable
            partition_key = None
            partition_strategy = None
            if table_data["is_partitioned"]:
                partition_info = self._extract_partition_info(table_data["oid"])
                partition_key = partition_info.get("partition_key")
                partition_strategy = partition_info.get("partition_strategy")
            
            # Create table object
            table = Table(
                name=name,
                schema=schema,
                oid=table_data["oid"],
                owner=table_data["owner"],
                created_at=table_data["created_at"] or datetime.now(),
                modified_at=table_data["modified_at"] or datetime.now(),
                comment=table_data["comment"],
                columns=columns,
                primary_key=primary_key,
                foreign_keys=foreign_keys,
                unique_constraints=unique_constraints,
                check_constraints=check_constraints,
                indexes=indexes,
                is_partitioned=table_data["is_partitioned"],
                partition_key=partition_key,
                partition_strategy=partition_strategy,
                estimated_row_count=table_data["estimated_row_count"],
                total_size_bytes=table_data["total_size_bytes"]
            )
            
            # Generate hash for the table definition
            definition = self._generate_table_definition(table)
            table.hash = self.generate_object_hash(definition)
            
            tables[qualified_name] = table
            
        self.logger.info(f"Extracted {len(tables)} tables")
        return tables
    
    def _extract_columns(self, table_oid: int) -> List[Column]:
        """
        Extract columns for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[Column]: List of columns
        """
        column_query = """
            SELECT 
                a.attname AS name,
                a.attnum AS position,
                pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                NOT a.attnotnull AS nullable,
                pg_get_expr(d.adbin, d.adrelid) AS default_value,
                col_description(a.attrelid, a.attnum) AS comment,
                CASE WHEN t.typtype = 'd' THEN t.typbasetype ELSE a.atttypid END AS base_type_oid,
                CASE WHEN t.typtype = 'd' THEN format_type(t.typbasetype, NULL) ELSE NULL END AS base_type_name,
                information_schema._pg_char_max_length(
                    CASE WHEN t.typtype = 'd' THEN t.typbasetype ELSE a.atttypid END, 
                    a.atttypmod
                ) AS character_length,
                information_schema._pg_numeric_precision(
                    CASE WHEN t.typtype = 'd' THEN t.typbasetype ELSE a.atttypid END, 
                    a.atttypmod
                ) AS numeric_precision,
                information_schema._pg_numeric_scale(
                    CASE WHEN t.typtype = 'd' THEN t.typbasetype ELSE a.atttypid END, 
                    a.atttypmod
                ) AS numeric_scale
            FROM 
                pg_attribute a
                JOIN pg_type t ON a.atttypid = t.oid
                LEFT JOIN pg_attrdef d ON (a.attrelid, a.attnum) = (d.adrelid, d.adnum)
            WHERE 
                a.attrelid = %(table_oid)s
                AND a.attnum > 0
                AND NOT a.attisdropped
            ORDER BY 
                a.attnum
        """
        
        column_results = self.execute_query(column_query, {"table_oid": table_oid})
        columns = []
        
        # Get primary key columns
        pk_columns = self._get_primary_key_columns(table_oid)
        
        # Get unique constraint columns
        unique_columns = self._get_unique_constraint_columns(table_oid)
        
        # Get foreign key columns
        fk_columns = self._get_foreign_key_columns(table_oid)
        
        for col_data in column_results:
            column = Column(
                name=col_data["name"],
                position=col_data["position"],
                data_type=col_data["data_type"],
                nullable=col_data["nullable"],
                default_value=col_data["default_value"],
                comment=col_data["comment"],
                is_primary_key=col_data["name"] in pk_columns,
                is_unique=col_data["name"] in unique_columns,
                is_foreign_key=col_data["name"] in fk_columns,
                character_length=col_data["character_length"],
                numeric_precision=col_data["numeric_precision"],
                numeric_scale=col_data["numeric_scale"]
            )
            columns.append(column)
            
        return columns
    
    def _get_primary_key_columns(self, table_oid: int) -> List[str]:
        """
        Get primary key column names for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[str]: List of primary key column names
        """
        pk_query = """
            SELECT 
                a.attname AS column_name
            FROM 
                pg_constraint c
                JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'p'
            ORDER BY 
                array_position(c.conkey, a.attnum)
        """
        
        pk_results = self.execute_query(pk_query, {"table_oid": table_oid})
        return [row["column_name"] for row in pk_results]
    
    def _extract_primary_key(self, table_oid: int) -> Optional[List[str]]:
        """
        Extract primary key column names for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            Optional[List[str]]: List of primary key column names or None
        """
        pk_columns = self._get_primary_key_columns(table_oid)
        return pk_columns if pk_columns else None
    
    def _get_unique_constraint_columns(self, table_oid: int) -> List[str]:
        """
        Get unique constraint column names for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[str]: List of unique constraint column names
        """
        unique_query = """
            SELECT 
                a.attname AS column_name
            FROM 
                pg_constraint c
                JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'u'
        """
        
        unique_results = self.execute_query(unique_query, {"table_oid": table_oid})
        return [row["column_name"] for row in unique_results]
    
    def _get_foreign_key_columns(self, table_oid: int) -> List[str]:
        """
        Get foreign key column names for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[str]: List of foreign key column names
        """
        fk_query = """
            SELECT 
                a.attname AS column_name
            FROM 
                pg_constraint c
                JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'f'
        """
        
        fk_results = self.execute_query(fk_query, {"table_oid": table_oid})
        return [row["column_name"] for row in fk_results]
    
    def _extract_foreign_keys(self, table_oid: int) -> List[Dict[str, Any]]:
        """
        Extract foreign key constraints for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[Dict[str, Any]]: List of foreign key constraints
        """
        fk_query = """
            SELECT 
                c.conname AS constraint_name,
                n2.nspname AS referenced_schema,
                c2.relname AS referenced_table,
                array_agg(a1.attname ORDER BY array_position(c.conkey, a1.attnum)) AS column_names,
                array_agg(a2.attname ORDER BY array_position(c.confkey, a2.attnum)) AS referenced_columns,
                c.confupdtype AS update_action,
                c.confdeltype AS delete_action,
                c.condeferrable AS is_deferrable,
                c.condeferred AS is_initially_deferred
            FROM 
                pg_constraint c
                JOIN pg_class c1 ON c1.oid = c.conrelid
                JOIN pg_namespace n1 ON n1.oid = c1.relnamespace
                JOIN pg_class c2 ON c2.oid = c.confrelid
                JOIN pg_namespace n2 ON n2.oid = c2.relnamespace
                JOIN pg_attribute a1 ON a1.attrelid = c.conrelid AND a1.attnum = ANY(c.conkey)
                JOIN pg_attribute a2 ON a2.attrelid = c.confrelid AND a2.attnum = ANY(c.confkey)
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'f'
            GROUP BY 
                c.conname, n2.nspname, c2.relname, c.confupdtype, c.confdeltype, c.condeferrable, c.condeferred
        """
        
        fk_results = self.execute_query(fk_query, {"table_oid": table_oid})
        foreign_keys = []
        
        for fk_data in fk_results:
            # Map action codes to names
            update_actions = {
                'a': 'NO ACTION',
                'r': 'RESTRICT',
                'c': 'CASCADE',
                'n': 'SET NULL',
                'd': 'SET DEFAULT'
            }
            
            delete_actions = {
                'a': 'NO ACTION',
                'r': 'RESTRICT',
                'c': 'CASCADE',
                'n': 'SET NULL',
                'd': 'SET DEFAULT'
            }
            
            foreign_key = {
                "constraint_name": fk_data["constraint_name"],
                "columns": fk_data["column_names"],
                "referenced_schema": fk_data["referenced_schema"],
                "referenced_table": fk_data["referenced_table"],
                "referenced_columns": fk_data["referenced_columns"],
                "update_action": update_actions.get(fk_data["update_action"], 'UNKNOWN'),
                "delete_action": delete_actions.get(fk_data["delete_action"], 'UNKNOWN'),
                "is_deferrable": fk_data["is_deferrable"],
                "is_initially_deferred": fk_data["is_initially_deferred"]
            }
            
            foreign_keys.append(foreign_key)
            
        return foreign_keys
    
    def _extract_unique_constraints(self, table_oid: int) -> List[Dict[str, Any]]:
        """
        Extract unique constraints for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[Dict[str, Any]]: List of unique constraints
        """
        unique_query = """
            SELECT 
                c.conname AS constraint_name,
                array_agg(a.attname ORDER BY array_position(c.conkey, a.attnum)) AS column_names,
                c.condeferrable AS is_deferrable,
                c.condeferred AS is_initially_deferred
            FROM 
                pg_constraint c
                JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'u'
            GROUP BY 
                c.conname, c.condeferrable, c.condeferred
        """
        
        unique_results = self.execute_query(unique_query, {"table_oid": table_oid})
        unique_constraints = []
        
        for uc_data in unique_results:
            unique_constraint = {
                "constraint_name": uc_data["constraint_name"],
                "columns": uc_data["column_names"],
                "is_deferrable": uc_data["is_deferrable"],
                "is_initially_deferred": uc_data["is_initially_deferred"]
            }
            
            unique_constraints.append(unique_constraint)
            
        return unique_constraints
    
    def _extract_check_constraints(self, table_oid: int) -> List[Dict[str, Any]]:
        """
        Extract check constraints for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[Dict[str, Any]]: List of check constraints
        """
        check_query = """
            SELECT 
                c.conname AS constraint_name,
                pg_get_constraintdef(c.oid) AS definition,
                c.condeferrable AS is_deferrable,
                c.condeferred AS is_initially_deferred,
                c.convalidated AS is_validated
            FROM 
                pg_constraint c
            WHERE 
                c.conrelid = %(table_oid)s
                AND c.contype = 'c'
        """
        
        check_results = self.execute_query(check_query, {"table_oid": table_oid})
        check_constraints = []
        
        for cc_data in check_results:
            check_constraint = {
                "constraint_name": cc_data["constraint_name"],
                "definition": cc_data["definition"],
                "is_deferrable": cc_data["is_deferrable"],
                "is_initially_deferred": cc_data["is_initially_deferred"],
                "is_validated": cc_data["is_validated"]
            }
            
            check_constraints.append(check_constraint)
            
        return check_constraints
    
    def _extract_indexes(self, table_oid: int) -> List[Dict[str, Any]]:
        """
        Extract indexes for a table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            List[Dict[str, Any]]: List of indexes
        """
        index_query = """
            SELECT 
                i.relname AS index_name,
                am.amname AS index_type,
                array_agg(a.attname ORDER BY array_position(ix.indkey, a.attnum)) AS column_names,
                ix.indisunique AS is_unique,
                ix.indisprimary AS is_primary,
                ix.indisexclusion AS is_exclusion,
                pg_get_indexdef(i.oid) AS definition
            FROM 
                pg_index ix
                JOIN pg_class i ON i.oid = ix.indexrelid
                JOIN pg_class t ON t.oid = ix.indrelid
                JOIN pg_am am ON am.oid = i.relam
                JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
            WHERE 
                t.oid = %(table_oid)s
            GROUP BY 
                i.relname, am.amname, ix.indisunique, ix.indisprimary, ix.indisexclusion, i.oid
        """
        
        index_results = self.execute_query(index_query, {"table_oid": table_oid})
        indexes = []
        
        for idx_data in index_results:
            index = {
                "index_name": idx_data["index_name"],
                "index_type": idx_data["index_type"],
                "columns": idx_data["column_names"],
                "is_unique": idx_data["is_unique"],
                "is_primary": idx_data["is_primary"],
                "is_exclusion": idx_data["is_exclusion"],
                "definition": idx_data["definition"]
            }
            
            indexes.append(index)
            
        return indexes
    
    def _extract_partition_info(self, table_oid: int) -> Dict[str, str]:
        """
        Extract partition information for a partitioned table.
        
        Args:
            table_oid: OID of the table
            
        Returns:
            Dict[str, str]: Partition key and strategy
        """
        partition_query = """
            SELECT 
                pg_get_partkeydef(%(table_oid)s::oid) AS partition_key,
                CASE partstrat
                    WHEN 'l' THEN 'LIST'
                    WHEN 'r' THEN 'RANGE'
                    WHEN 'h' THEN 'HASH'
                    ELSE 'UNKNOWN'
                END AS partition_strategy
            FROM 
                pg_partitioned_table
            WHERE 
                partrelid = %(table_oid)s
        """
        
        partition_results = self.execute_query(partition_query, {"table_oid": table_oid})
        
        if partition_results:
            return {
                "partition_key": partition_results[0]["partition_key"],
                "partition_strategy": partition_results[0]["partition_strategy"]
            }
        
        return {"partition_key": None, "partition_strategy": None}
    
    def _generate_table_definition(self, table: Table) -> str:
        """
        Generate a standardized table definition for hashing.
        
        Args:
            table: Table object
            
        Returns:
            str: Table definition
        """
        parts = [f"CREATE TABLE {table.schema}.{table.name} ("]
        
        # Add columns
        column_defs = []
        for col in sorted(table.columns, key=lambda c: c.position):
            col_def = f"{col.name} {col.data_type}"
            
            if not col.nullable:
                col_def += " NOT NULL"
                
            if col.default_value:
                col_def += f" DEFAULT {col.default_value}"
                
            column_defs.append(col_def)
            
        parts.append(",\n  ".join(column_defs))
        
        # Add primary key
        if table.primary_key:
            pk_cols = ", ".join(table.primary_key)
            parts.append(f",\n  PRIMARY KEY ({pk_cols})")
            
        # Add unique constraints
        for uc in table.unique_constraints:
            uc_cols = ", ".join(uc["columns"])
            parts.append(f",\n  CONSTRAINT {uc['constraint_name']} UNIQUE ({uc_cols})")
            
        # Add foreign keys
        for fk in table.foreign_keys:
            fk_cols = ", ".join(fk["columns"])
            ref_cols = ", ".join(fk["referenced_columns"])
            parts.append(
                f",\n  CONSTRAINT {fk['constraint_name']} FOREIGN KEY ({fk_cols}) "
                f"REFERENCES {fk['referenced_schema']}.{fk['referenced_table']} ({ref_cols}) "
                f"ON UPDATE {fk['update_action']} ON DELETE {fk['delete_action']}"
            )
            
        # Add check constraints
        for cc in table.check_constraints:
            parts.append(f",\n  CONSTRAINT {cc['constraint_name']} {cc['definition']}")
            
        parts.append("\n)")
        
        # Add partition clause if applicable
        if table.is_partitioned and table.partition_key and table.partition_strategy:
            parts.append(f" PARTITION BY {table.partition_strategy} ({table.partition_key})")

        # Indexes and comments participate in the fingerprint.
        #
        # They did not, which meant dropping an index or rewriting a column
        # comment produced an identical hash and the change was reported as "no
        # change". hash_utils explicitly says a changed comment is a real change
        # worth surfacing, so leaving them out contradicted the documented
        # behaviour. Sorted so ordering from the catalogue cannot alter the hash.
        for idx in sorted(table.indexes or [], key=lambda i: i.get("index_name", "")):
            parts.append(f"\n  INDEX {idx.get('index_name')} {idx.get('definition', '')}")

        if table.comment:
            parts.append(f"\n  COMMENT ON TABLE IS {table.comment}")

        for col in sorted(table.columns, key=lambda c: c.position):
            if getattr(col, "comment", None):
                parts.append(f"\n  COMMENT ON COLUMN {col.name} IS {col.comment}")

        return "".join(parts)
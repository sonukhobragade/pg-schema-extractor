"""
Base extractor class for PostgreSQL database objects.
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

import psycopg2
from psycopg2.extras import RealDictCursor

from src.models.database_objects import BaseDBObject
from src.utils.hash_utils import generate_hash


class BaseExtractor(ABC):
    """
    Abstract base class for all database object extractors.
    
    This class provides common functionality for connecting to a PostgreSQL
    database and extracting schema objects. Specific extractors for tables,
    functions, etc. should inherit from this class.
    """
    
    def __init__(
        self, 
        host: str, 
        port: int, 
        dbname: str, 
        user: str, 
        password: str,
        exclude_schemas: List[str] = None,
        exclude_patterns: List[str] = None
    ):
        """
        Initialize the extractor with database connection parameters.
        
        Args:
            host: Database host
            port: Database port
            dbname: Database name
            user: Database user
            password: Database password
            exclude_schemas: List of schemas to exclude
            exclude_patterns: List of name patterns to exclude
        """
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.exclude_schemas = exclude_schemas or ["pg_catalog", "information_schema"]
        self.exclude_patterns = exclude_patterns or []
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def get_connection(self):
        """
        Create and return a database connection.
        
        Returns:
            psycopg2.connection: Database connection
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                cursor_factory=RealDictCursor
            )
            return conn
        except Exception as e:
            self.logger.error(f"Failed to connect to database: {e}")
            raise
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a SQL query and return the results.
        
        Args:
            query: SQL query to execute
            params: Query parameters
            
        Returns:
            List[Dict[str, Any]]: Query results
        """
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute(query, params or {})
                results = cur.fetchall()
                return [dict(row) for row in results]
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            self.logger.debug(f"Query: {query}")
            self.logger.debug(f"Params: {params}")
            raise
        finally:
            if conn:
                conn.close()
    
    def should_include_object(self, schema: str, name: str) -> bool:
        """
        Check if an object should be included based on exclusion rules.
        
        Args:
            schema: Schema name
            name: Object name
            
        Returns:
            bool: True if the object should be included
        """
        # Check excluded schemas
        if schema in self.exclude_schemas:
            return False
        
        # Check excluded patterns
        for pattern in self.exclude_patterns:
            if pattern.endswith('%'):
                prefix = pattern[:-1]
                if name.startswith(prefix):
                    return False
            elif pattern.startswith('%'):
                suffix = pattern[1:]
                if name.endswith(suffix):
                    return False
            elif pattern == name:
                return False
        
        return True
    
    def generate_object_hash(self, definition: str) -> str:
        """
        Generate a hash for an object definition.
        
        Args:
            definition: Object definition string
            
        Returns:
            str: Hash of the definition
        """
        return generate_hash(definition)
    
    @abstractmethod
    def extract(self) -> Dict[str, BaseDBObject]:
        """
        Extract database objects.
        
        Returns:
            Dict[str, BaseDBObject]: Dictionary of extracted objects by qualified name
        """
        pass
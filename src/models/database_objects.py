"""
Pydantic models for PostgreSQL database objects.
"""

from datetime import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class BaseDBObject(BaseModel):
    """Base model for all database objects."""
    
    name: str = Field(..., description="Name of the database object")
    schema: str = Field(..., description="Schema name")
    oid: int = Field(..., description="PostgreSQL object identifier")
    owner: str = Field(..., description="Owner of the object")
    created_at: datetime = Field(..., description="Creation timestamp")
    modified_at: datetime = Field(..., description="Last modification timestamp")
    comment: Optional[str] = Field(None, description="Object comment")
    hash: Optional[str] = Field(None, description="Hash of the object definition")


class Column(BaseModel):
    """Database column model."""
    
    name: str = Field(..., description="Column name")
    position: int = Field(..., description="Position in table")
    data_type: str = Field(..., description="Data type")
    nullable: bool = Field(..., description="Whether column allows NULL values")
    default_value: Optional[str] = Field(None, description="Default value expression")
    comment: Optional[str] = Field(None, description="Column comment")
    is_primary_key: bool = Field(False, description="Whether column is part of primary key")
    is_unique: bool = Field(False, description="Whether column has unique constraint")
    is_foreign_key: bool = Field(False, description="Whether column is a foreign key")
    character_length: Optional[int] = Field(None, description="Character length for string types")
    numeric_precision: Optional[int] = Field(None, description="Precision for numeric types")
    numeric_scale: Optional[int] = Field(None, description="Scale for numeric types")


class Table(BaseDBObject):
    """Database table model."""
    
    columns: List[Column] = Field(default_factory=list, description="Table columns")
    primary_key: Optional[List[str]] = Field(None, description="Primary key column names")
    foreign_keys: List[Dict[str, Any]] = Field(default_factory=list, description="Foreign key constraints")
    unique_constraints: List[Dict[str, Any]] = Field(default_factory=list, description="Unique constraints")
    check_constraints: List[Dict[str, Any]] = Field(default_factory=list, description="Check constraints")
    indexes: List[Dict[str, Any]] = Field(default_factory=list, description="Table indexes")
    is_partitioned: bool = Field(False, description="Whether table is partitioned")
    partition_key: Optional[str] = Field(None, description="Partition key if partitioned")
    partition_strategy: Optional[str] = Field(None, description="Partition strategy if partitioned")
    estimated_row_count: Optional[int] = Field(None, description="Estimated row count")
    total_size_bytes: Optional[int] = Field(None, description="Total size in bytes")


class Function(BaseDBObject):
    """Database function model."""
    
    language: str = Field(..., description="Function language (e.g., SQL, plpgsql)")
    return_type: str = Field(..., description="Return data type")
    arguments: List[Dict[str, str]] = Field(default_factory=list, description="Function arguments")
    definition: str = Field(..., description="Function definition")
    volatility: str = Field("VOLATILE", description="Function volatility (VOLATILE, STABLE, IMMUTABLE)")
    is_strict: bool = Field(False, description="Whether function is strict (returns NULL if any arg is NULL)")
    is_security_definer: bool = Field(False, description="Whether function executes with definer's privileges")
    config_params: Dict[str, str] = Field(default_factory=dict, description="Configuration parameters")


class Trigger(BaseDBObject):
    """Database trigger model."""
    
    table_name: str = Field(..., description="Table the trigger is defined on")
    table_schema: str = Field(..., description="Schema of the table")
    function_name: str = Field(..., description="Function called by trigger")
    function_schema: str = Field(..., description="Schema of the function")
    events: List[str] = Field(..., description="Events that fire the trigger (INSERT, UPDATE, DELETE)")
    activation: str = Field(..., description="When trigger fires (BEFORE, AFTER, INSTEAD OF)")
    for_each: str = Field(..., description="ROW or STATEMENT")
    condition: Optional[str] = Field(None, description="Optional WHEN condition")
    is_enabled: bool = Field(True, description="Whether trigger is enabled")


class Constraint(BaseDBObject):
    """Database constraint model."""
    
    table_name: str = Field(..., description="Table the constraint is defined on")
    table_schema: str = Field(..., description="Schema of the table")
    constraint_type: str = Field(..., description="Type of constraint (PRIMARY KEY, FOREIGN KEY, etc.)")
    definition: str = Field(..., description="Constraint definition")
    is_deferrable: bool = Field(False, description="Whether constraint is deferrable")
    is_initially_deferred: bool = Field(False, description="Whether constraint is initially deferred")
    is_validated: bool = Field(True, description="Whether constraint is validated")


class View(BaseDBObject):
    """Database view model."""
    
    definition: str = Field(..., description="View definition (query)")
    is_updatable: bool = Field(False, description="Whether view is updatable")
    is_materialized: bool = Field(False, description="Whether view is materialized")
    refresh_mode: Optional[str] = Field(None, description="Refresh mode for materialized views")
    columns: List[Dict[str, Any]] = Field(default_factory=list, description="View columns")


class Sequence(BaseDBObject):
    """Database sequence model."""
    
    data_type: str = Field(..., description="Data type of sequence")
    start_value: int = Field(..., description="Start value")
    min_value: int = Field(..., description="Minimum value")
    max_value: int = Field(..., description="Maximum value")
    increment_by: int = Field(..., description="Increment value")
    cycle: bool = Field(False, description="Whether sequence cycles")
    cache_size: int = Field(1, description="Cache size")
    last_value: Optional[int] = Field(None, description="Last value")


class DatabaseSchema(BaseModel):
    """Complete database schema model."""
    
    database_name: str = Field(..., description="Database name")
    version: str = Field(..., description="Schema version identifier")
    extracted_at: datetime = Field(..., description="Extraction timestamp")
    tables: Dict[str, Table] = Field(default_factory=dict, description="Tables by qualified name")
    functions: Dict[str, Function] = Field(default_factory=dict, description="Functions by qualified name")
    triggers: Dict[str, Trigger] = Field(default_factory=dict, description="Triggers by qualified name")
    constraints: Dict[str, Constraint] = Field(default_factory=dict, description="Constraints by qualified name")
    views: Dict[str, View] = Field(default_factory=dict, description="Views by qualified name")
    sequences: Dict[str, Sequence] = Field(default_factory=dict, description="Sequences by qualified name")
    schemas: List[str] = Field(default_factory=list, description="List of schemas in the database")
    extensions: Dict[str, Any] = Field(default_factory=dict, description="Installed extensions")
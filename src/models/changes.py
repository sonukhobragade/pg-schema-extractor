"""
Pydantic models for database change detection.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

from src.models.database_objects import BaseDBObject


class ChangeType(str, Enum):
    """Types of changes that can be detected."""
    
    CREATED = "created"
    MODIFIED = "modified"
    DELETED = "deleted"


class ChangeImpact(str, Enum):
    """Impact levels for changes."""
    
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class ObjectType(str, Enum):
    """Types of database objects."""
    
    TABLE = "table"
    FUNCTION = "function"
    TRIGGER = "trigger"
    CONSTRAINT = "constraint"
    VIEW = "view"
    SEQUENCE = "sequence"
    COLUMN = "column"
    INDEX = "index"
    FOREIGN_KEY = "foreign_key"


class AttributeChange(BaseModel):
    """Represents a change to a specific attribute."""
    
    attribute_name: str = Field(..., description="Name of the changed attribute")
    old_value: Optional[Any] = Field(None, description="Previous value")
    new_value: Optional[Any] = Field(None, description="New value")
    impact: ChangeImpact = Field(ChangeImpact.LOW, description="Impact level of this change")


class ObjectChange(BaseModel):
    """Represents a change to a database object."""
    
    object_type: ObjectType = Field(..., description="Type of database object")
    object_name: str = Field(..., description="Name of the object")
    schema_name: str = Field(..., description="Schema name")
    qualified_name: str = Field(..., description="Fully qualified name (schema.name)")
    change_type: ChangeType = Field(..., description="Type of change")
    timestamp: datetime = Field(..., description="When the change was detected")
    attribute_changes: List[AttributeChange] = Field(
        default_factory=list, 
        description="List of attribute changes"
    )
    old_object: Optional[BaseDBObject] = Field(None, description="Previous state of the object")
    new_object: Optional[BaseDBObject] = Field(None, description="New state of the object")
    impact: ChangeImpact = Field(ChangeImpact.LOW, description="Overall impact of this change")
    
    @property
    def has_attribute_changes(self) -> bool:
        """Check if there are any attribute changes."""
        return len(self.attribute_changes) > 0


class ChangeSet(BaseModel):
    """A collection of changes between two database states."""
    
    id: str = Field(..., description="Unique identifier for this change set")
    database_name: str = Field(..., description="Database name")
    from_version: str = Field(..., description="Source schema version")
    to_version: str = Field(..., description="Target schema version")
    created_at: datetime = Field(..., description="When the change set was created")
    changes: List[ObjectChange] = Field(default_factory=list, description="List of changes")
    
    @property
    def total_changes(self) -> int:
        """Get the total number of changes."""
        return len(self.changes)
    
    @property
    def changes_by_type(self) -> Dict[ChangeType, List[ObjectChange]]:
        """Group changes by change type."""
        result = {ct: [] for ct in ChangeType}
        for change in self.changes:
            result[change.change_type].append(change)
        return result
    
    @property
    def changes_by_object_type(self) -> Dict[ObjectType, List[ObjectChange]]:
        """Group changes by object type."""
        result = {ot: [] for ot in ObjectType}
        for change in self.changes:
            result[change.object_type].append(change)
        return result
    
    @property
    def changes_by_impact(self) -> Dict[ChangeImpact, List[ObjectChange]]:
        """Group changes by impact level."""
        result = {il: [] for il in ChangeImpact}
        for change in self.changes:
            result[change.impact].append(change)
        return result


class ChangeStatistics(BaseModel):
    """Statistical summary of a change set."""
    
    total_changes: int = Field(0, description="Total number of changes")
    created_count: int = Field(0, description="Number of created objects")
    modified_count: int = Field(0, description="Number of modified objects")
    deleted_count: int = Field(0, description="Number of deleted objects")
    high_impact_count: int = Field(0, description="Number of high impact changes")
    medium_impact_count: int = Field(0, description="Number of medium impact changes")
    low_impact_count: int = Field(0, description="Number of low impact changes")
    changes_by_object_type: Dict[str, int] = Field(
        default_factory=dict, 
        description="Count of changes by object type"
    )
"""
Pydantic models for AI analysis results.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from src.models.changes import ChangeImpact


class RiskLevel(str, Enum):
    """Risk levels for database changes."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


class RiskCategory(str, Enum):
    """Categories of risks that can be identified."""
    
    SECURITY = "security"
    PERFORMANCE = "performance"
    DATA_INTEGRITY = "data_integrity"
    BACKWARD_COMPATIBILITY = "backward_compatibility"
    BUSINESS_LOGIC = "business_logic"
    COMPLIANCE = "compliance"
    OPERATIONAL = "operational"


class Recommendation(BaseModel):
    """Recommendation for addressing a risk."""
    
    title: str = Field(..., description="Short title for the recommendation")
    description: str = Field(..., description="Detailed description of the recommendation")
    code_example: Optional[str] = Field(None, description="Example code if applicable")
    priority: int = Field(1, description="Priority (1-5, with 1 being highest)")
    effort_estimate: Optional[str] = Field(None, description="Estimated effort to implement")


class Risk(BaseModel):
    """Identified risk in a database change."""
    
    id: str = Field(..., description="Unique identifier for this risk")
    title: str = Field(..., description="Short title describing the risk")
    description: str = Field(..., description="Detailed description of the risk")
    level: RiskLevel = Field(..., description="Risk level")
    categories: List[RiskCategory] = Field(..., description="Risk categories")
    affected_objects: List[str] = Field(..., description="Qualified names of affected objects")
    related_changes: List[str] = Field(..., description="IDs of related changes")
    recommendations: List[Recommendation] = Field(
        default_factory=list, 
        description="Recommendations to address the risk"
    )
    confidence: float = Field(..., description="AI confidence score (0.0-1.0)")


class BusinessImpact(BaseModel):
    """Business impact analysis of a change."""
    
    description: str = Field(..., description="Description of the business impact")
    affected_features: List[str] = Field(default_factory=list, description="Affected application features")
    affected_services: List[str] = Field(default_factory=list, description="Affected services")
    affected_users: List[str] = Field(default_factory=list, description="Types of affected users")
    severity: ChangeImpact = Field(..., description="Severity of the business impact")


class PerformanceImpact(BaseModel):
    """Performance impact analysis of a change."""
    
    description: str = Field(..., description="Description of the performance impact")
    query_complexity_change: Optional[str] = Field(None, description="Change in query complexity")
    estimated_latency_change: Optional[str] = Field(None, description="Estimated change in latency")
    index_usage_impact: Optional[str] = Field(None, description="Impact on index usage")
    scaling_concerns: Optional[str] = Field(None, description="Concerns about scaling")
    severity: ChangeImpact = Field(..., description="Severity of the performance impact")


class SecurityImpact(BaseModel):
    """Security impact analysis of a change."""
    
    description: str = Field(..., description="Description of the security impact")
    vulnerability_introduced: bool = Field(False, description="Whether a vulnerability is introduced")
    vulnerability_type: Optional[str] = Field(None, description="Type of vulnerability if introduced")
    data_exposure_risk: bool = Field(False, description="Risk of data exposure")
    permission_changes: List[str] = Field(default_factory=list, description="Changes to permissions")
    severity: ChangeImpact = Field(..., description="Severity of the security impact")


class ComplianceImpact(BaseModel):
    """Compliance impact analysis of a change."""
    
    description: str = Field(..., description="Description of the compliance impact")
    regulations_affected: List[str] = Field(default_factory=list, description="Affected regulations")
    data_governance_impact: Optional[str] = Field(None, description="Impact on data governance")
    audit_implications: Optional[str] = Field(None, description="Implications for auditing")
    severity: ChangeImpact = Field(..., description="Severity of the compliance impact")


class AIAnalysisResult(BaseModel):
    """Complete AI analysis result for a change set."""
    
    id: str = Field(..., description="Unique identifier for this analysis")
    change_set_id: str = Field(..., description="ID of the analyzed change set")
    created_at: datetime = Field(..., description="When the analysis was created")
    model_used: str = Field(..., description="AI model used for analysis")
    risks: List[Risk] = Field(default_factory=list, description="Identified risks")
    business_impacts: Dict[str, BusinessImpact] = Field(
        default_factory=dict, 
        description="Business impacts by object qualified name"
    )
    performance_impacts: Dict[str, PerformanceImpact] = Field(
        default_factory=dict, 
        description="Performance impacts by object qualified name"
    )
    security_impacts: Dict[str, SecurityImpact] = Field(
        default_factory=dict, 
        description="Security impacts by object qualified name"
    )
    compliance_impacts: Dict[str, ComplianceImpact] = Field(
        default_factory=dict, 
        description="Compliance impacts by object qualified name"
    )
    summary: str = Field(..., description="Overall summary of the analysis")
    
    @property
    def has_critical_risks(self) -> bool:
        """Check if there are any critical risks."""
        return any(risk.level == RiskLevel.CRITICAL for risk in self.risks)
    
    @property
    def has_high_risks(self) -> bool:
        """Check if there are any high risks."""
        return any(risk.level == RiskLevel.HIGH for risk in self.risks)
    
    @property
    def risk_count_by_level(self) -> Dict[RiskLevel, int]:
        """Count risks by level."""
        result = {level: 0 for level in RiskLevel}
        for risk in self.risks:
            result[risk.level] += 1
        return result
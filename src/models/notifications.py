"""
Pydantic models for notification system.
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, EmailStr

from src.models.changes import ChangeSet
from src.models.ai_analysis import AIAnalysisResult, RiskLevel


class NotificationChannel(str, Enum):
    """Available notification channels."""
    
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"


class NotificationPriority(str, Enum):
    """Priority levels for notifications."""
    
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class NotificationStatus(str, Enum):
    """Status of a notification."""
    
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    ACKNOWLEDGED = "acknowledged"


class EmailRecipient(BaseModel):
    """Email recipient model."""
    
    email: EmailStr = Field(..., description="Email address")
    name: Optional[str] = Field(None, description="Recipient name")
    role: Optional[str] = Field(None, description="Recipient role")


class SlackDestination(BaseModel):
    """Slack destination model."""
    
    channel: str = Field(..., description="Slack channel")
    workspace: Optional[str] = Field(None, description="Slack workspace")


class WebhookDestination(BaseModel):
    """Webhook destination model."""
    
    url: str = Field(..., description="Webhook URL")
    headers: Dict[str, str] = Field(default_factory=dict, description="HTTP headers")
    auth_token: Optional[str] = Field(None, description="Authentication token")


class SMSRecipient(BaseModel):
    """SMS recipient model."""
    
    phone_number: str = Field(..., description="Phone number")
    name: Optional[str] = Field(None, description="Recipient name")


class NotificationDestination(BaseModel):
    """Combined notification destination model."""
    
    channel: NotificationChannel = Field(..., description="Notification channel")
    email_recipients: Optional[List[EmailRecipient]] = Field(None, description="Email recipients")
    slack_destination: Optional[SlackDestination] = Field(None, description="Slack destination")
    webhook_destination: Optional[WebhookDestination] = Field(None, description="Webhook destination")
    sms_recipients: Optional[List[SMSRecipient]] = Field(None, description="SMS recipients")


class NotificationTemplate(BaseModel):
    """Template for generating notifications."""
    
    id: str = Field(..., description="Template identifier")
    name: str = Field(..., description="Template name")
    subject_template: str = Field(..., description="Subject template")
    body_template: str = Field(..., description="Body template")
    format: str = Field("markdown", description="Template format (markdown, html, plain)")
    variables: List[str] = Field(default_factory=list, description="Available template variables")


class Notification(BaseModel):
    """Notification model."""
    
    id: str = Field(..., description="Unique notification ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    sent_at: Optional[datetime] = Field(None, description="When notification was sent")
    acknowledged_at: Optional[datetime] = Field(None, description="When notification was acknowledged")
    priority: NotificationPriority = Field(..., description="Notification priority")
    status: NotificationStatus = Field(NotificationStatus.PENDING, description="Notification status")
    subject: str = Field(..., description="Notification subject")
    body: str = Field(..., description="Notification body")
    destinations: List[NotificationDestination] = Field(..., description="Notification destinations")
    change_set_id: Optional[str] = Field(None, description="Related change set ID")
    analysis_id: Optional[str] = Field(None, description="Related analysis ID")
    template_id: Optional[str] = Field(None, description="Template ID used")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    error_message: Optional[str] = Field(None, description="Error message if sending failed")


class NotificationRule(BaseModel):
    """Rule for when to send notifications."""
    
    id: str = Field(..., description="Rule identifier")
    name: str = Field(..., description="Rule name")
    description: Optional[str] = Field(None, description="Rule description")
    enabled: bool = Field(True, description="Whether rule is enabled")
    
    # Conditions
    min_risk_level: RiskLevel = Field(RiskLevel.HIGH, description="Minimum risk level to trigger")
    min_changes_count: Optional[int] = Field(None, description="Minimum number of changes to trigger")
    object_types: Optional[List[str]] = Field(None, description="Object types to monitor")
    schemas: Optional[List[str]] = Field(None, description="Schemas to monitor")
    
    # Actions
    priority: NotificationPriority = Field(NotificationPriority.MEDIUM, description="Notification priority")
    template_id: str = Field(..., description="Template ID to use")
    destinations: List[NotificationDestination] = Field(..., description="Where to send notifications")
    
    def should_notify(self, change_set: ChangeSet, analysis: AIAnalysisResult) -> bool:
        """
        Determine if a notification should be sent based on this rule.
        
        Args:
            change_set: The change set to evaluate
            analysis: The AI analysis result
            
        Returns:
            bool: True if notification should be sent
        """
        # Check if rule is enabled
        if not self.enabled:
            return False
            
        # Check risk level
        has_sufficient_risk = False
        for risk in analysis.risks:
            risk_levels = {
                RiskLevel.CRITICAL: 4,
                RiskLevel.HIGH: 3,
                RiskLevel.MEDIUM: 2,
                RiskLevel.LOW: 1,
                RiskLevel.NONE: 0
            }
            
            if risk_levels[risk.level] >= risk_levels[self.min_risk_level]:
                has_sufficient_risk = True
                break
                
        if not has_sufficient_risk:
            return False
            
        # Check changes count
        if self.min_changes_count is not None and change_set.total_changes < self.min_changes_count:
            return False
            
        # Check object types
        if self.object_types is not None:
            matching_objects = False
            for change in change_set.changes:
                if change.object_type in self.object_types:
                    matching_objects = True
                    break
                    
            if not matching_objects:
                return False
                
        # Check schemas
        if self.schemas is not None:
            matching_schemas = False
            for change in change_set.changes:
                if change.schema_name in self.schemas:
                    matching_schemas = True
                    break
                    
            if not matching_schemas:
                return False
                
        return True
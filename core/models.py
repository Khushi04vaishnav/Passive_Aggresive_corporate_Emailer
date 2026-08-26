from enum import Enum

from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    LOW = "LOW"
    REVIEW = "REVIEW"
    BLOCKED = "BLOCKED"


class RiskResult(BaseModel):
    """Aggregated output of the Safety Shield for one piece of text."""

    risk_level: RiskLevel
    risk_score: int = Field(ge=0, le=100)
    toxicity_detected: bool = False
    confidential_data_detected: bool = False
    prompt_injection_detected: bool = False
    unsafe_request_detected: bool = False
    requires_human_review: bool = False
    reasons: list[str] = Field(default_factory=list)

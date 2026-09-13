from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class IncidentCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10)
    requester: str = Field(min_length=2, max_length=150)
    area: str = Field(min_length=2, max_length=100)
    category: str | None = None
    impact_users: int = Field(default=1, ge=1)
    urgency: str = Field(default="media")


class IncidentUpdate(BaseModel):
    status: str = Field(min_length=3, max_length=50)


class IncidentAIAnalysisRequest(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    description: str = Field(min_length=10)


class IncidentAIAnalysisResponse(BaseModel):
    title: str
    description: str
    analysis: str


class IncidentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    requester: str
    area: str
    category: str | None
    status: str
    priority: str
    impact_users: int
    urgency: str
    ai_category: str | None
    ai_priority: str | None
    ai_confidence: float | None
    created_at: datetime
    updated_at: datetime

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class JoinRequestCreate(BaseModel):
    message: Optional[str] = Field(default=None, max_length=500)


class JoinRequestDecision(BaseModel):
    action: str = Field(pattern="^(approved|rejected)$")


class JoinRequestOut(BaseModel):
    id: int
    party_id: int
    attendee_id: int
    message: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttendeeOut(BaseModel):
    id: int
    party_id: int
    user_id: int
    approved_at: datetime

    class Config:
        from_attributes = True

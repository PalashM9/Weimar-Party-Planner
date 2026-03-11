from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PartyCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: Optional[str] = None
    party_date: datetime
    address: str = Field(min_length=3, max_length=255)
    city: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_guests: Optional[int] = Field(default=None, ge=1)
    is_private: bool = False


class PartyUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=150)
    description: Optional[str] = None
    party_date: Optional[datetime] = None
    address: Optional[str] = Field(default=None, min_length=3, max_length=255)
    city: Optional[str] = Field(default=None, min_length=2, max_length=100)
    country: Optional[str] = Field(default=None, min_length=2, max_length=100)
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    max_guests: Optional[int] = Field(default=None, ge=1)
    is_private: Optional[bool] = None
    status: Optional[str] = Field(default=None, max_length=50)


class PartyOut(BaseModel):
    id: int
    host_id: int
    title: str
    description: Optional[str]
    party_date: datetime
    address: str
    city: str
    country: str
    latitude: Optional[float]
    longitude: Optional[float]
    max_guests: Optional[int]
    is_private: bool
    status: str
    map_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

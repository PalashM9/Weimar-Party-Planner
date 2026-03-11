from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func
from app.db.base import Base


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    party_date = Column(DateTime(timezone=True), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    max_guests = Column(Integer, nullable=True)
    is_private = Column(Boolean, default=False, nullable=False)
    status = Column(String(50), default="scheduled", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

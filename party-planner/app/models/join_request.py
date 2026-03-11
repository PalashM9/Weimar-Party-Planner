from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base


class JoinRequest(Base):
    __tablename__ = "join_requests"
    __table_args__ = (
        UniqueConstraint("party_id", "attendee_id", name="uq_join_request_party_attendee"),
    )

    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False, index=True)
    attendee_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    message = Column(Text, nullable=True)
    status = Column(String(50), default="pending", nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

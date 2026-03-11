from sqlalchemy import Column, DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base


class Attendee(Base):
    __tablename__ = "attendees"
    __table_args__ = (
        UniqueConstraint("party_id", "user_id", name="uq_attendee_party_user"),
    )

    id = Column(Integer, primary_key=True, index=True)
    party_id = Column(Integer, ForeignKey("parties.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    approved_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

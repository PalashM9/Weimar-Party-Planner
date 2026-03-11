from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_host
from app.db.session import get_db
from app.models.attendee import Attendee
from app.models.join_request import JoinRequest
from app.models.party import Party
from app.models.user import User
from app.schemas.join_request import (
    AttendeeOut,
    JoinRequestCreate,
    JoinRequestDecision,
    JoinRequestOut,
)

router = APIRouter(prefix="/party-requests", tags=["Party Requests"])


@router.post("/{party_id}", response_model=JoinRequestOut, status_code=status.HTTP_201_CREATED)
def request_to_join(
    party_id: int,
    request_in: JoinRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.host_id == current_user.id:
        raise HTTPException(status_code=400, detail="Host cannot request to join own party")

    existing_attendee = db.query(Attendee).filter(
        Attendee.party_id == party_id,
        Attendee.user_id == current_user.id
    ).first()
    if existing_attendee:
        raise HTTPException(status_code=400, detail="You are already approved for this party")

    existing_request = db.query(JoinRequest).filter(
        JoinRequest.party_id == party_id,
        JoinRequest.attendee_id == current_user.id
    ).first()
    if existing_request:
        raise HTTPException(status_code=400, detail="Join request already exists")

    join_request = JoinRequest(
        party_id=party_id,
        attendee_id=current_user.id,
        message=request_in.message,
        status="pending"
    )
    db.add(join_request)
    db.commit()
    db.refresh(join_request)
    return join_request


@router.get("/host/pending", response_model=List[JoinRequestOut])
def list_pending_requests_for_host(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_host)
):
    pending_requests = (
        db.query(JoinRequest)
        .join(Party, Party.id == JoinRequest.party_id)
        .filter(Party.host_id == current_user.id, JoinRequest.status == "pending")
        .all()
    )
    return pending_requests


@router.put("/{request_id}/decision", response_model=JoinRequestOut)
def decide_join_request(
    request_id: int,
    decision: JoinRequestDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_host)
):
    join_request = (
        db.query(JoinRequest)
        .join(Party, Party.id == JoinRequest.party_id)
        .filter(JoinRequest.id == request_id, Party.host_id == current_user.id)
        .first()
    )

    if not join_request:
        raise HTTPException(status_code=404, detail="Join request not found")

    if join_request.status != "pending":
        raise HTTPException(status_code=400, detail="This request has already been processed")

    join_request.status = decision.action

    if decision.action == "approved":
        existing_attendee = db.query(Attendee).filter(
            Attendee.party_id == join_request.party_id,
            Attendee.user_id == join_request.attendee_id
        ).first()

        if not existing_attendee:
            attendee = Attendee(
                party_id=join_request.party_id,
                user_id=join_request.attendee_id
            )
            db.add(attendee)

    db.commit()
    db.refresh(join_request)
    return join_request


@router.get("/party/{party_id}/attendees", response_model=List[AttendeeOut])
def list_party_attendees(
    party_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only the host can view attendees")

    attendees = db.query(Attendee).filter(Attendee.party_id == party_id).all()
    return attendees

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_host
from app.db.session import get_db
from app.models.party import Party
from app.models.user import User
from app.schemas.party import PartyCreate, PartyOut, PartyUpdate
from app.services.map_service import build_osm_map_url

router = APIRouter(prefix="/parties", tags=["Parties"])


def to_party_out(party: Party) -> PartyOut:
    full_address = f"{party.address}, {party.city}, {party.country}"
    return PartyOut(
        id=party.id,
        host_id=party.host_id,
        title=party.title,
        description=party.description,
        party_date=party.party_date,
        address=party.address,
        city=party.city,
        country=party.country,
        latitude=party.latitude,
        longitude=party.longitude,
        max_guests=party.max_guests,
        is_private=party.is_private,
        status=party.status,
        map_url=build_osm_map_url(party.latitude, party.longitude, full_address),
        created_at=party.created_at,
        updated_at=party.updated_at,
    )


@router.post("", response_model=PartyOut, status_code=status.HTTP_201_CREATED)
def create_party(
    party_in: PartyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_host)
):
    party = Party(
        host_id=current_user.id,
        title=party_in.title,
        description=party_in.description,
        party_date=party_in.party_date,
        address=party_in.address,
        city=party_in.city,
        country=party_in.country,
        latitude=party_in.latitude,
        longitude=party_in.longitude,
        max_guests=party_in.max_guests,
        is_private=party_in.is_private,
        status="scheduled"
    )
    db.add(party)
    db.commit()
    db.refresh(party)
    return to_party_out(party)


@router.get("", response_model=List[PartyOut])
def list_parties(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.is_host:
        parties = db.query(Party).filter(Party.host_id == current_user.id).all()
    else:
        parties = db.query(Party).filter(Party.is_private == False).all()
    return [to_party_out(party) for party in parties]


@router.get("/{party_id}", response_model=PartyOut)
def get_party(
    party_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    party = db.query(Party).filter(Party.id == party_id).first()
    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    if party.is_private and party.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed to view this private party")

    return to_party_out(party)


@router.put("/{party_id}", response_model=PartyOut)
def update_party(
    party_id: int,
    party_in: PartyUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_host)
):
    party = db.query(Party).filter(
        Party.id == party_id,
        Party.host_id == current_user.id
    ).first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    update_data = party_in.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(party, field, value)

    db.commit()
    db.refresh(party)
    return to_party_out(party)


@router.delete("/{party_id}", status_code=status.HTTP_200_OK)
def delete_party(
    party_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_host)
):
    party = db.query(Party).filter(
        Party.id == party_id,
        Party.host_id == current_user.id
    ).first()

    if not party:
        raise HTTPException(status_code=404, detail="Party not found")

    db.delete(party)
    db.commit()
    return {"message": "Party deleted successfully"}

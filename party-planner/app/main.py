from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import User, Party, JoinRequest, Attendee
from app.api.routes_auth import router as auth_router
from app.api.routes_parties import router as parties_router
from app.api.routes_requests import router as requests_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)
app.include_router(parties_router)
app.include_router(requests_router)


@app.get("/")
def root():
    return {"message": "Party Planner API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}

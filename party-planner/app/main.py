from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.api.routes_auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Party Planner API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.repositories.request_repository import list_requests, request_summary
from src.schemas import UserErrorRequestOut

router = APIRouter(prefix="/requests", tags=["requests"])


@router.get("", response_model=list[UserErrorRequestOut])
def get_requests(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    return list_requests(db, limit=limit, offset=offset)


@router.get("/summary")
def get_requests_summary(db: Session = Depends(get_db)):
    return request_summary(db)

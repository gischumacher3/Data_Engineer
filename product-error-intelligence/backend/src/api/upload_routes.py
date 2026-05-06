from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.ingestion.upload_service import process_upload
from src.schemas import PipelineRunOut

router = APIRouter(prefix="/upload", tags=["upload"])


@router.post("", response_model=PipelineRunOut)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        return await process_upload(file, db)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

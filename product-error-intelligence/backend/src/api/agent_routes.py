from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.agents.product_gap_agent import analyze_product_gaps
from src.config.database import get_db

router = APIRouter(prefix="/agent", tags=["agent"])


@router.post("/analyze")
def analyze(db: Session = Depends(get_db)):
    return analyze_product_gaps(db)

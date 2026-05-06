from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.models.kpi_model import PipelineKPI


def latest_kpis(db: Session) -> PipelineKPI | None:
    return db.query(PipelineKPI).order_by(desc(PipelineKPI.created_at)).first()

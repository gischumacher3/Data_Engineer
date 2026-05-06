from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.models.pipeline_model import PipelineRun


def list_pipeline_runs(db: Session) -> list[PipelineRun]:
    return db.query(PipelineRun).order_by(desc(PipelineRun.started_at)).limit(25).all()


def get_pipeline_run(db: Session, run_id: str) -> PipelineRun | None:
    return db.get(PipelineRun, UUID(run_id))


def latest_pipeline_run(db: Session) -> PipelineRun | None:
    return db.query(PipelineRun).order_by(desc(PipelineRun.started_at)).first()

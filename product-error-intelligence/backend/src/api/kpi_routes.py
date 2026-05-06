from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.analytics.charts_service import count_by_category, count_by_severity, daily_errors
from src.analytics.kpi_service import get_dashboard_kpis
from src.config.database import get_db
from src.repositories.pipeline_run_repository import get_pipeline_run, list_pipeline_runs
from src.schemas import PipelineRunOut

router = APIRouter(tags=["analytics"])


@router.get("/kpis")
def get_kpis(db: Session = Depends(get_db)):
    return get_dashboard_kpis(db)


@router.get("/charts/categories")
def get_categories_chart(db: Session = Depends(get_db)):
    return count_by_category(db)


@router.get("/charts/severity")
def get_severity_chart(db: Session = Depends(get_db)):
    return count_by_severity(db)


@router.get("/charts/daily")
def get_daily_chart(db: Session = Depends(get_db)):
    return daily_errors(db)


@router.get("/pipeline-runs", response_model=list[PipelineRunOut])
def get_pipeline_runs(db: Session = Depends(get_db)):
    return list_pipeline_runs(db)


@router.get("/pipeline-runs/{run_id}", response_model=PipelineRunOut | None)
def get_pipeline_run_by_id(run_id: str, db: Session = Depends(get_db)):
    return get_pipeline_run(db, run_id)

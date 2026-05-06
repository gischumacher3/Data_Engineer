from sqlalchemy.orm import Session

from src.repositories.kpi_repository import latest_kpis
from src.repositories.request_repository import request_summary


def get_dashboard_kpis(db: Session) -> dict[str, object]:
    kpis = latest_kpis(db)
    summary = request_summary(db)
    return {
        **summary,
        "data_completeness": float(kpis.data_completeness) if kpis else 0,
        "duplicate_rate": float(kpis.duplicate_rate) if kpis else 0,
        "ingestion_success_rate": float(kpis.ingestion_success_rate) if kpis else 0,
        "pipeline_latency_seconds": float(kpis.pipeline_latency_seconds) if kpis else 0,
        "throughput_per_minute": float(kpis.throughput_per_minute) if kpis else 0,
        "top_error_coverage": float(kpis.top_error_coverage) if kpis else 0,
    }

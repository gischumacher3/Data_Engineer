import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class PipelineKPI(Base):
    __tablename__ = "pipeline_kpis"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pipeline_run_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("pipeline_runs.id"))
    data_completeness: Mapped[float | None] = mapped_column(Numeric(5, 2))
    ingestion_success_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    duplicate_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    schema_drift_incidents: Mapped[int] = mapped_column(Integer, default=0)
    pipeline_latency_seconds: Mapped[float | None] = mapped_column(Numeric(10, 2))
    processing_failure_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    throughput_per_minute: Mapped[float | None] = mapped_column(Numeric(10, 2))
    standardization_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    top_error_coverage: Mapped[float | None] = mapped_column(Numeric(5, 2))
    insight_generation_rate: Mapped[float | None] = mapped_column(Numeric(10, 2))
    time_to_insight_seconds: Mapped[float | None] = mapped_column(Numeric(10, 2))
    mttr_hours: Mapped[float | None] = mapped_column(Numeric(10, 2))
    error_recurrence_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

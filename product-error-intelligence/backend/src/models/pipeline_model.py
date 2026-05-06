import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, Numeric, String, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name: Mapped[str | None] = mapped_column(String)
    total_rows: Mapped[int] = mapped_column(Integer, default=0)
    valid_rows: Mapped[int] = mapped_column(Integer, default=0)
    invalid_rows: Mapped[int] = mapped_column(Integer, default=0)
    duplicate_rows: Mapped[int] = mapped_column(Integer, default=0)
    completeness_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    duplicate_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    ingestion_success_rate: Mapped[float | None] = mapped_column(Numeric(5, 2))
    pipeline_latency_seconds: Mapped[float | None] = mapped_column(Numeric(10, 2))
    status: Mapped[str] = mapped_column(String, default="running")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime)

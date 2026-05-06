import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, Text, Uuid
from sqlalchemy.orm import Mapped, mapped_column

from src.config.database import Base


class UserErrorRequest(Base):
    __tablename__ = "user_error_requests"

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    client_name: Mapped[str | None] = mapped_column(String)
    email: Mapped[str | None] = mapped_column(String)
    document_number: Mapped[str | None] = mapped_column(String)
    phone: Mapped[str | None] = mapped_column(String)
    company: Mapped[str | None] = mapped_column(String)
    problem_description: Mapped[str] = mapped_column(Text)
    request_date: Mapped[datetime | None] = mapped_column(DateTime)
    is_finished: Mapped[bool | None] = mapped_column(Boolean)
    problem_category: Mapped[str | None] = mapped_column(String)
    problem_subcategory: Mapped[str | None] = mapped_column(String)
    severity: Mapped[str | None] = mapped_column(String)
    customer_profile: Mapped[str | None] = mapped_column(String)
    is_duplicate: Mapped[bool] = mapped_column(Boolean, default=False)
    data_quality_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    business_impact_score: Mapped[float | None] = mapped_column(Numeric(5, 2))
    source_file_name: Mapped[str | None] = mapped_column(String)
    pipeline_run_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("pipeline_runs.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

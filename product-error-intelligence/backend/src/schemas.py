from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PipelineRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    file_name: str | None
    total_rows: int
    valid_rows: int
    invalid_rows: int
    duplicate_rows: int
    completeness_rate: float | None
    duplicate_rate: float | None
    ingestion_success_rate: float | None
    pipeline_latency_seconds: float | None
    status: str
    started_at: datetime
    finished_at: datetime | None


class UserErrorRequestOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    client_name: str | None
    email: str | None
    document_number: str | None
    phone: str | None
    company: str | None
    problem_description: str
    request_date: datetime | None
    is_finished: bool | None
    problem_category: str | None
    problem_subcategory: str | None
    severity: str | None
    customer_profile: str | None
    is_duplicate: bool
    data_quality_score: float | None
    business_impact_score: float | None
    source_file_name: str | None
    pipeline_run_id: UUID | None
    created_at: datetime
    updated_at: datetime

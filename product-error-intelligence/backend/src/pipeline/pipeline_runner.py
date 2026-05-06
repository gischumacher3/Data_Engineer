import time
from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from src.models.kpi_model import PipelineKPI
from src.models.pipeline_model import PipelineRun
from src.models.request_model import UserErrorRequest
from src.pipeline.cleaner import clean_dataframe
from src.pipeline.enrichment import enrich_dataframe
from src.pipeline.standardizer import standardize_columns
from src.pipeline.validator import validate_dataframe


def run_pipeline(df: pd.DataFrame, file_name: str, db: Session) -> PipelineRun:
    started = time.perf_counter()
    standardized = standardize_columns(df)
    validation = validate_dataframe(standardized)

    pipeline_run = PipelineRun(file_name=file_name, total_rows=len(df), status="running")
    db.add(pipeline_run)
    db.flush()

    if validation.missing_columns:
        pipeline_run.status = "failed"
        pipeline_run.invalid_rows = len(df)
        pipeline_run.finished_at = datetime.utcnow()
        db.commit()
        raise ValueError(f"CSV sem colunas obrigatórias: {', '.join(validation.missing_columns)}")

    cleaned = clean_dataframe(standardized)
    enriched = enrich_dataframe(cleaned)
    valid_rows = len(enriched)
    duplicate_rows = int(enriched["is_duplicate"].sum())
    latency = round(time.perf_counter() - started, 2)

    for record in enriched.to_dict(orient="records"):
        db.add(
            UserErrorRequest(
                client_name=_value(record.get("client_name")),
                email=_value(record.get("email")),
                document_number=_value(record.get("document_number")),
                phone=_value(record.get("phone")),
                company=_value(record.get("company")),
                problem_description=record["problem_description"],
                request_date=_date_value(record.get("request_date")),
                is_finished=_value(record.get("is_finished")),
                problem_category=record.get("problem_category"),
                problem_subcategory=record.get("problem_subcategory"),
                severity=record.get("severity"),
                customer_profile=record.get("customer_profile"),
                is_duplicate=bool(record.get("is_duplicate")),
                data_quality_score=record.get("data_quality_score"),
                business_impact_score=record.get("business_impact_score"),
                source_file_name=file_name,
                pipeline_run_id=pipeline_run.id,
            )
        )

    pipeline_run.valid_rows = valid_rows
    pipeline_run.invalid_rows = max(len(df) - valid_rows, validation.empty_required_rows)
    pipeline_run.duplicate_rows = duplicate_rows
    pipeline_run.completeness_rate = _rate(valid_rows, len(df))
    pipeline_run.duplicate_rate = _rate(duplicate_rows, max(valid_rows, 1))
    pipeline_run.ingestion_success_rate = _rate(valid_rows, len(df))
    pipeline_run.pipeline_latency_seconds = latency
    pipeline_run.status = "success"
    pipeline_run.finished_at = datetime.utcnow()

    db.add(_build_kpis(pipeline_run, enriched, latency))
    db.commit()
    db.refresh(pipeline_run)
    return pipeline_run


def _build_kpis(pipeline_run: PipelineRun, df: pd.DataFrame, latency: float) -> PipelineKPI:
    total = max(len(df), 1)
    top_category_count = int(df["problem_category"].value_counts().iloc[0]) if len(df) else 0
    duplicate_count = int(df["is_duplicate"].sum()) if len(df) else 0
    return PipelineKPI(
        pipeline_run_id=pipeline_run.id,
        data_completeness=round(float(df["data_quality_score"].mean()), 2) if len(df) else 0,
        ingestion_success_rate=pipeline_run.ingestion_success_rate,
        duplicate_rate=pipeline_run.duplicate_rate,
        schema_drift_incidents=0,
        pipeline_latency_seconds=latency,
        processing_failure_rate=_rate(pipeline_run.invalid_rows, pipeline_run.total_rows),
        throughput_per_minute=round(total / max(latency, 0.01) * 60, 2),
        standardization_rate=100,
        top_error_coverage=_rate(top_category_count, total),
        insight_generation_rate=100,
        time_to_insight_seconds=latency,
        mttr_hours=0,
        error_recurrence_rate=_rate(duplicate_count, total),
    )


def _rate(part: int | float, total: int | float) -> float:
    return round((part / total) * 100, 2) if total else 0


def _value(value: object) -> object | None:
    return None if pd.isna(value) else value


def _date_value(value: object) -> datetime | None:
    if pd.isna(value):
        return None
    return pd.Timestamp(value).to_pydatetime()

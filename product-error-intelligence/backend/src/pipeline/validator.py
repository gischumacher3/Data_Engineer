from dataclasses import dataclass

import pandas as pd

from src.pipeline.standardizer import REQUIRED_COLUMNS


@dataclass
class ValidationResult:
    is_valid: bool
    missing_columns: list[str]
    empty_required_rows: int
    invalid_date_rows: int
    duplicate_rows: int


def validate_dataframe(df: pd.DataFrame) -> ValidationResult:
    missing = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing:
        return ValidationResult(False, missing, 0, 0, 0)

    empty_required_rows = int(df[list(REQUIRED_COLUMNS)].isna().any(axis=1).sum())
    invalid_dates = int(pd.to_datetime(df["request_date"], errors="coerce").isna().sum())
    duplicate_rows = int(df.duplicated(subset=["email", "problem_description", "request_date"]).sum())

    return ValidationResult(
        is_valid=empty_required_rows < len(df),
        missing_columns=[],
        empty_required_rows=empty_required_rows,
        invalid_date_rows=invalid_dates,
        duplicate_rows=duplicate_rows,
    )

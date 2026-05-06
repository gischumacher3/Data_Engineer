from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.request_model import UserErrorRequest


def count_by_category(db: Session) -> list[dict[str, object]]:
    rows = (
        db.query(UserErrorRequest.problem_category, func.count(UserErrorRequest.id))
        .group_by(UserErrorRequest.problem_category)
        .order_by(func.count(UserErrorRequest.id).desc())
        .all()
    )
    return [{"name": name or "Sem categoria", "value": total} for name, total in rows]


def count_by_severity(db: Session) -> list[dict[str, object]]:
    rows = (
        db.query(UserErrorRequest.severity, func.count(UserErrorRequest.id))
        .group_by(UserErrorRequest.severity)
        .order_by(func.count(UserErrorRequest.id).desc())
        .all()
    )
    return [{"name": name or "Sem severidade", "value": total} for name, total in rows]


def daily_errors(db: Session) -> list[dict[str, object]]:
    rows = (
        db.query(func.date(UserErrorRequest.request_date), func.count(UserErrorRequest.id))
        .filter(UserErrorRequest.request_date.isnot(None))
        .group_by(func.date(UserErrorRequest.request_date))
        .order_by(func.date(UserErrorRequest.request_date))
        .all()
    )
    return [{"date": str(date), "total": total} for date, total in rows]

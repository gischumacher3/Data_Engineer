from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from src.models.request_model import UserErrorRequest


def list_requests(db: Session, limit: int = 100, offset: int = 0) -> list[UserErrorRequest]:
    return (
        db.query(UserErrorRequest)
        .order_by(desc(UserErrorRequest.created_at))
        .offset(offset)
        .limit(limit)
        .all()
    )


def request_summary(db: Session) -> dict[str, object]:
    total = db.query(func.count(UserErrorRequest.id)).scalar() or 0
    finished = db.query(func.count(UserErrorRequest.id)).filter(UserErrorRequest.is_finished.is_(True)).scalar() or 0
    critical = db.query(func.count(UserErrorRequest.id)).filter(UserErrorRequest.severity == "Crítico").scalar() or 0
    avg_impact = db.query(func.avg(UserErrorRequest.business_impact_score)).scalar() or 0
    top_category = (
        db.query(UserErrorRequest.problem_category, func.count(UserErrorRequest.id).label("total"))
        .group_by(UserErrorRequest.problem_category)
        .order_by(desc("total"))
        .first()
    )
    return {
        "total_requests": total,
        "finished_rate": round((finished / total) * 100, 2) if total else 0,
        "critical_errors": critical,
        "average_business_impact": round(float(avg_impact), 2),
        "top_category": top_category[0] if top_category else None,
    }

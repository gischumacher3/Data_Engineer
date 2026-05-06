from sqlalchemy.orm import Session

from src.analytics.insights_service import build_rule_based_insights


def get_product_error_context(db: Session) -> dict[str, object]:
    return build_rule_based_insights(db)

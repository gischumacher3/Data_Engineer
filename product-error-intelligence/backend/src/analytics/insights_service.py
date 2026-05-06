from sqlalchemy.orm import Session

from src.analytics.charts_service import count_by_category, count_by_severity
from src.analytics.kpi_service import get_dashboard_kpis


def build_rule_based_insights(db: Session) -> dict[str, object]:
    kpis = get_dashboard_kpis(db)
    categories = count_by_category(db)
    severities = count_by_severity(db)
    top_categories = categories[:3]
    critical_count = next((item["value"] for item in severities if item["name"] == "Crítico"), 0)

    recommendations = []
    if critical_count:
        recommendations.append("Priorizar incidentes críticos antes de melhorias incrementais de UX.")
    if any(item["name"] == "Login" for item in top_categories):
        recommendations.append("Investigar fluxo de autenticação, SSO e expiração de sessão.")
    if any(item["name"] == "Falta de conhecimento das features" for item in top_categories):
        recommendations.append("Criar conteúdo educativo e melhorar discovery das funcionalidades.")
    if not recommendations:
        recommendations.append("Monitorar recorrência por categoria antes de promover itens para o backlog.")

    summary = (
        f"Os principais problemas se concentram em "
        f"{', '.join(str(item['name']) for item in top_categories) or 'categorias ainda não classificadas'}. "
        f"A categoria mais frequente é {kpis.get('top_category') or 'indefinida'} e o impacto médio está em "
        f"{kpis.get('average_business_impact', 0)}."
    )
    return {"summary": summary, "recommendations": recommendations, "kpis": kpis, "top_categories": top_categories}

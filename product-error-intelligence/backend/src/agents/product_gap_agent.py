from sqlalchemy.orm import Session

from src.agents.prompts import PRODUCT_GAP_ANALYSIS_PROMPT
from src.agents.tools import get_product_error_context
from src.config.settings import get_settings


def analyze_product_gaps(db: Session) -> dict[str, object]:
    context = get_product_error_context(db)
    settings = get_settings()

    if not settings.openai_api_key:
        return {
            "provider": "rule_based",
            "analysis": context["summary"],
            "recommendations": context["recommendations"],
            "context": context,
        }

    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat

        agent = Agent(
            model=OpenAIChat(id="gpt-4o-mini", api_key=settings.openai_api_key),
            instructions=PRODUCT_GAP_ANALYSIS_PROMPT,
            markdown=True,
        )
        response = agent.run(f"Contexto estruturado para análise: {context}")
        return {
            "provider": "agno_openai",
            "analysis": response.content,
            "recommendations": context["recommendations"],
            "context": context,
        }
    except Exception as exc:
        return {
            "provider": "rule_based_fallback",
            "analysis": context["summary"],
            "recommendations": [*context["recommendations"], f"Agno indisponível no momento: {exc}"],
            "context": context,
        }

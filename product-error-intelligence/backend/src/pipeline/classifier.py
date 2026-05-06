import re


CATEGORY_RULES = {
    "Portal fora do ar": ["fora do ar", "indisponivel", "indisponível", "timeout", "503", "502"],
    "Login": ["não consigo acessar", "nao consigo acessar", "login", "sessão expirada", "sessao expirada", "sso"],
    "Primeiro acesso": ["primeiro acesso", "link expirado", "e-mail não chegou", "email não chegou", "email nao chegou"],
    "Restaurar senha": ["senha", "reset", "restaurar", "recuperar acesso"],
    "Dados incorretos": ["cnpj", "cpf", "dados errados", "histórico sumiu", "historico sumiu", "cadastro incorreto"],
    "Usuário não encontrado": ["usuário não encontrado", "usuario nao encontrado", "user not found"],
    "Bugs": ["bug", "erro", "falha", "travando", "quebra"],
    "Falta de conhecimento das features": ["como faço", "como faco", "onde encontro", "não sei usar", "nao sei usar"],
}

SEVERITY_BY_CATEGORY = {
    "Portal fora do ar": "Crítico",
    "Login": "Alto",
    "Dados incorretos": "Alto",
    "Usuário não encontrado": "Alto",
    "Restaurar senha": "Médio",
    "Primeiro acesso": "Médio",
    "Bugs": "Médio",
    "Falta de conhecimento das features": "Baixo",
}

SEVERITY_SCORE = {"Crítico": 100, "Alto": 75, "Médio": 45, "Baixo": 20}


def classify_problem(description: str) -> dict[str, object]:
    text = _normalize(description)
    matches: list[tuple[str, int]] = []

    for category, keywords in CATEGORY_RULES.items():
        score = sum(1 for keyword in keywords if _normalize(keyword) in text)
        if score:
            matches.append((category, score))

    if not matches:
        category = "Bugs"
        confidence = 0.35
    else:
        category, score = sorted(matches, key=lambda item: item[1], reverse=True)[0]
        confidence = min(0.95, 0.55 + (score * 0.15))

    severity = SEVERITY_BY_CATEGORY.get(category, "Médio")
    return {
        "problem_category": category,
        "problem_subcategory": _subcategory_for(text, category),
        "severity": severity,
        "classification_confidence": confidence,
    }


def business_impact_score(category_volume: int, severity: str, customer_profile: str, recurrence: int) -> float:
    volume_score = min(category_volume * 10, 100)
    severity_score = SEVERITY_SCORE.get(severity, 45)
    profile_score = {"Enterprise": 100, "Mid-market": 65, "SMB": 35}.get(customer_profile, 45)
    recurrence_score = min(recurrence * 15, 100)
    return round((volume_score * 0.4) + (severity_score * 0.3) + (profile_score * 0.2) + (recurrence_score * 0.1), 2)


def infer_customer_profile(company: str | None) -> str:
    if not company:
        return "SMB"
    text = company.lower()
    if any(token in text for token in ["enterprise", "holding", "grupo", "corp"]):
        return "Enterprise"
    if any(token in text for token in ["ltda", "sa", "s/a"]):
        return "Mid-market"
    return "SMB"


def _normalize(value: str) -> str:
    text = value.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _subcategory_for(text: str, category: str) -> str:
    if category == "Login" and "sso" in text:
        return "SSO"
    if category == "Portal fora do ar" and ("503" in text or "502" in text):
        return "Erro HTTP 5xx"
    if category == "Dados incorretos" and ("cnpj" in text or "cpf" in text):
        return "Documento"
    return "Geral"

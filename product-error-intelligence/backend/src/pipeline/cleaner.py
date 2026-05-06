import pandas as pd


BOOLEAN_TRUE = {"sim", "s", "yes", "y", "true", "1", "finalizada", "concluida", "concluída"}
BOOLEAN_FALSE = {"não", "nao", "n", "no", "false", "0", "aberta", "pendente"}


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in cleaned.select_dtypes(include="object").columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()

    cleaned["email"] = cleaned["email"].str.lower()
    cleaned["document_number"] = cleaned["document_number"].str.replace(r"\D", "", regex=True)
    cleaned["phone"] = cleaned["phone"].str.replace(r"\D", "", regex=True)
    cleaned["request_date"] = pd.to_datetime(cleaned["request_date"], errors="coerce")
    cleaned["is_finished"] = cleaned["is_finished"].map(_to_bool)
    cleaned["problem_description"] = cleaned["problem_description"].fillna("").astype(str).str.strip()
    cleaned["is_duplicate"] = cleaned.duplicated(subset=["email", "problem_description", "request_date"], keep="first")

    return cleaned[cleaned["problem_description"] != ""].copy()


def _to_bool(value: object) -> bool | None:
    if pd.isna(value):
        return None
    text = str(value).strip().lower()
    if text in BOOLEAN_TRUE:
        return True
    if text in BOOLEAN_FALSE:
        return False
    return None

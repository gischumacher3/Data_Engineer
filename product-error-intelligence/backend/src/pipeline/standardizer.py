import pandas as pd
import unicodedata


COLUMN_MAPPING = {
    "Nome do cliente": "client_name",
    "Email": "email",
    "CPF/CNPJ": "document_number",
    "Telefone": "phone",
    "Empresa": "company",
    "Problema (Descrição)": "problem_description",
    "Data da Solicitação": "request_date",
    "Solicitação Finalizada?": "is_finished",
}

REQUIRED_COLUMNS = set(COLUMN_MAPPING.values())


def _normalize_header(value: object) -> str:
    text = str(value).replace("\ufeff", "").strip().lower()
    text = text.replace("\u00a0", " ")
    text = " ".join(text.split())
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return "".join(ch for ch in text if ch.isalnum())


_NORMALIZED_COLUMN_MAPPING = {_normalize_header(key): value for key, value in COLUMN_MAPPING.items()}
_NORMALIZED_COLUMN_MAPPING |= {_normalize_header(value): value for value in REQUIRED_COLUMNS}


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    stripped = df.rename(columns={column: str(column).strip() for column in df.columns})
    rename_map: dict[object, str] = {}
    for column in stripped.columns:
        normalized = _normalize_header(column)
        mapped = _NORMALIZED_COLUMN_MAPPING.get(normalized)
        if mapped:
            rename_map[column] = mapped
    return stripped.rename(columns=rename_map)

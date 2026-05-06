import pandas as pd

from src.pipeline.classifier import business_impact_score, classify_problem, infer_customer_profile


def enrich_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    enriched = df.copy()
    classifications = enriched["problem_description"].apply(classify_problem).apply(pd.Series)
    enriched = pd.concat([enriched, classifications], axis=1)
    enriched["customer_profile"] = enriched["company"].apply(infer_customer_profile)

    category_counts = enriched["problem_category"].value_counts().to_dict()
    recurrence_counts = enriched.groupby(["email", "problem_category"])["problem_category"].transform("count")

    enriched["data_quality_score"] = enriched.apply(_quality_score, axis=1)
    enriched["business_impact_score"] = enriched.apply(
        lambda row: business_impact_score(
            int(category_counts.get(row["problem_category"], 1)),
            row["severity"],
            row["customer_profile"],
            int(recurrence_counts.loc[row.name]),
        ),
        axis=1,
    )
    return enriched


def _quality_score(row: pd.Series) -> float:
    columns = ["client_name", "email", "document_number", "phone", "company", "problem_description", "request_date"]
    completed = sum(0 if pd.isna(row[column]) or row[column] == "" else 1 for column in columns)
    return round((completed / len(columns)) * 100, 2)

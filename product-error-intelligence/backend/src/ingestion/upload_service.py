from fastapi import UploadFile
from sqlalchemy.orm import Session

from src.ingestion.csv_reader import read_csv_upload
from src.pipeline.pipeline_runner import run_pipeline


async def process_upload(file: UploadFile, db: Session):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise ValueError("O arquivo precisa estar em formato CSV.")
    df = await read_csv_upload(file)
    return run_pipeline(df, file.filename, db)

from io import BytesIO

import pandas as pd
from fastapi import UploadFile


async def read_csv_upload(file: UploadFile) -> pd.DataFrame:
    content = await file.read()
    try:
        return pd.read_csv(BytesIO(content), sep=None, engine="python")
    except UnicodeDecodeError:
        return pd.read_csv(BytesIO(content), sep=None, engine="python", encoding="latin1")

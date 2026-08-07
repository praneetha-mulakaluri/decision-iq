import pandas as pd
from fastapi import HTTPException, UploadFile
from pandas.errors import EmptyDataError

async def process_csv(file: UploadFile):

    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload a CSV file"
        )

    try:
        df = pd.read_csv(file.file)

        if df.empty:
            raise HTTPException(
                status_code=400,
                detail="CSV contains no data."
            )

        return {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": list(df.columns),
            "data_types": df.dtypes.astype(str).to_dict(),
            "missing_values": df.isnull().sum().to_dict()
        }

    except EmptyDataError:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV is empty."
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
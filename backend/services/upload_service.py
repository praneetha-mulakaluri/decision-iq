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
            "summary": {
                "rows": df.shape[0],
                "columns": df.shape[1],
                "memory_usage": int(df.memory_usage(deep=True).sum()),
                "duplicate_rows": int(df.duplicated().sum())
            },
            "schema": {
                "column_names": list(df.columns),
                "data_types": df.dtypes.astype(str).to_dict(),
                "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
                "categorical_columns": df.select_dtypes(include=['object', 'category']).columns.tolist()
            },
            "data_quality": {
                "missing_values": df.isnull().sum().to_dict(),
                "missing_values_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
                "duplicate_rows_percentage": (df.duplicated().sum() / len(df) * 100),
                "unique_values": {col: df[col].nunique() for col in df.columns}
            }
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
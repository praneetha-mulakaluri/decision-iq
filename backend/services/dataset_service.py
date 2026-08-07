import pandas as pd
from fastapi import HTTPException, UploadFile
from pandas.errors import EmptyDataError

from models.statistics import Statistics
from models.summary import Summary
from models.dataQuality import DataQuality
from models.dataQuality import DataQuality
from models.schema import Schema

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

        summary = Summary(
            rows=df.shape[0],
            columns=df.shape[1],
            memory_usage=int(df.memory_usage(deep=True).sum()),
            duplicate_rows=int(df.duplicated().sum())
        )
        schema = Schema(
            columnNames=list(df.columns),
            dataTypes=df.dtypes.astype(str).to_dict(),
            numericColumns=df.select_dtypes(include=['number']).columns.tolist(),
            categoricalColumns=df.select_dtypes(include=['object', 'category']).columns.tolist()
        )
        data_quality = DataQuality(
            missingValues=df.isnull().sum().to_dict(),
            missingValuesPercentage=(df.isnull().sum() / len(df) * 100).to_dict(),
            uniqueValues={col: df[col].nunique() for col in df.columns},
            duplicateRowsPercentage=(df.duplicated().sum() / len(df) * 100)
        )

        numeric_df = df.select_dtypes(include=["number"])
        statistics = {}

        for column in numeric_df.columns:
            statistics[column] = Statistics(
                mean=float(numeric_df[column].mean()),
                median=float(numeric_df[column].median()),
                mode=float(numeric_df[column].mode().iloc[0]),
                min=float(numeric_df[column].min()),
                max=float(numeric_df[column].max()),
                std_dev=float(numeric_df[column].std()),
                variance=float(numeric_df[column].var())
            )

        return {
            "summary": summary,
            "schema": schema,
            "dataQuality": data_quality,
            "statistics": statistics
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
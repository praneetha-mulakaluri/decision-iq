import pandas as pd
from fastapi import HTTPException, UploadFile
from pandas.errors import EmptyDataError

from models.preprocessing import Preprocessing
from services import preprocessing_service
from models.statistics import Statistics
from models.summary import Summary
from models.datasetProfileRespone import DatasetProfileResponse
from models.dataQuality import Dataquality
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
            memory_usage_bytes=int(df.memory_usage(deep=True).sum()),
            duplicate_rows=int(df.duplicated().sum())
        )
        schema = Schema(
            column_names=list(df.columns),
            data_types=df.dtypes.astype(str).to_dict(),
            numeric_columns=df.select_dtypes(include=['number']).columns.tolist(),
            categorical_columns=df.select_dtypes(include=['object', 'category']).columns.tolist()
        )
        data_quality = Dataquality(
            missing_values=df.isnull().sum().to_dict(),
            missing_values_percentage=(df.isnull().sum() / len(df) * 100).to_dict(),
            unique_values={col: df[col].nunique() for col in df.columns},
            duplicate_rows_percentage=(df.duplicated().sum() / len(df) * 100)
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

        df, missing_values_filled = preprocessing_service.fill_missing_values(df)
        df, duplicates_removed = preprocessing_service.drop_duplicates(df)
        df, scaled_columns = preprocessing_service.scale_numeric_columns(df)
        df, encoded_columns = preprocessing_service.encode_categorical_columns(df)

        preprocessing = Preprocessing(
            duplicates_removed=duplicates_removed,
            missing_values_filled=missing_values_filled,
            encoded_columns=encoded_columns,
            scaled_columns=scaled_columns,
        )

        return DatasetProfileResponse(
            summary=summary,
            schema=schema,
            data_quality=data_quality,
            statistics=statistics,
            preprocessing=preprocessing
        )

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
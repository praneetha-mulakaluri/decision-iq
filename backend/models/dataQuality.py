from pydantic import BaseModel


class DataQuality(BaseModel):
    missingValues: dict[str, int]
    missingValuesPercentage: dict[str, float]
    uniqueValues: dict[str, int]
    duplicateRowsPercentage: float
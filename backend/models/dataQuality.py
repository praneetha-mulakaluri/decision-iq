from pydantic import BaseModel


class Dataquality(BaseModel):
    missing_values: dict[str, int]
    missing_values_percentage: dict[str, float]
    unique_values: dict[str, int]
    duplicate_rows_percentage: float
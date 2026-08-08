from pydantic import BaseModel


class Schema(BaseModel):
    column_names: list[str]
    data_types: dict[str, str]
    numeric_columns: list[str]
    categorical_columns: list[str]
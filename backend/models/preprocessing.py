from pydantic import BaseModel


class Preprocessing(BaseModel):
    duplicates_removed: int
    missing_values_filled: dict[str, str]
    encoded_columns: list[str]
    scaled_columns: list[str]




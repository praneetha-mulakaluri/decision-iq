from pydantic import BaseModel


class Summary(BaseModel):
    rows: int
    columns: int
    memory_usage_bytes: int
    duplicate_rows: int
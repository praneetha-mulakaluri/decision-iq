from pydantic import BaseModel


class Summary(BaseModel):
    rows: int
    columns: int
    memory_usage: int
    duplicate_rows: int
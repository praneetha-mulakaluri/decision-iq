from pydantic import BaseModel


class Schema(BaseModel):
    columnNames: list[str]
    dataTypes: dict[str, str]
    numericColumns: list[str]
    categoricalColumns: list[str]
from pydantic import BaseModel

from models.statistics import Statistics
from models.summary import Summary
from models.dataQuality import DataQuality
from models.schema import Schema


class DatasetProfileResponse(BaseModel):
    summary: Summary
    schema: Schema
    dataQuality: DataQuality
    statistics: dict[str, Statistics] # Nested dictionary to hold statistics for each column

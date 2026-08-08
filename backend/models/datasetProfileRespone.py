from pydantic import BaseModel

from models.preprocessing import Preprocessing
from models.statistics import Statistics
from models.summary import Summary
from models.dataQuality import Dataquality
from models.schema import Schema


class DatasetProfileResponse(BaseModel):
    summary: Summary
    schema: Schema
    data_quality: Dataquality
    statistics: dict[str, Statistics]
    preprocessing: Preprocessing

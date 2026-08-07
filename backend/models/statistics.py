from pydantic import BaseModel


class Statistics(BaseModel):
    mean: float
    median: float
    mode: float | None
    min: float
    max: float
    std_dev: float
    variance: float
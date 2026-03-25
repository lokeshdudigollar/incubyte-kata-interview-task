from pydantic import BaseModel


class SalaryMetricsByCountryResponse(BaseModel):
    country: str
    min_salary: float | None
    max_salary: float | None
    average_salary: float | None


class SalaryMetricsByJobTitleResponse(BaseModel):
    job_title: str
    average_salary: float | None

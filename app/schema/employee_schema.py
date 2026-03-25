from pydantic import BaseModel, ConfigDict, Field


class EmployeeCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    job_title: str = Field(..., min_length=1)
    country: str = Field(..., min_length=1)
    salary: float = Field(..., gt=0)


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    job_title: str
    country: str
    salary: float

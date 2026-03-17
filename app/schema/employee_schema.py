from pydantic import BaseModel, ConfigDict

class EmployeeCreate(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    job_title: str
    country: str
    salary: float
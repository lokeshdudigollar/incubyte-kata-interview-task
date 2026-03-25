from pydantic import BaseModel

class SalaryResponse(BaseModel):
    gross_salary: float
    deduction: int
    net_salary: float
from pydantic import BaseModel

class SalaryResponse(BaseModel):
    employee_id: int
    gross_salary: float
    deduction: int
    net_salary: float
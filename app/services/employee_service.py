from fastapi import HTTPException
from app.repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def create_employee(self, full_name, job_title, country, salary):
        # we can add any business logic here before creating the employee
        return self.repo.create_employee(
            full_name=full_name,
            job_title=job_title,
            country=country,
            salary=salary
        )
    
    def get_employee(self, employee_id: int):
        employee = self.repo.get_employee(employee_id)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        return employee
    
    def calculate_salary(self, employee_id: int):
        employee = self.get_employee(employee_id)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        gross = employee.salary
        # Example salary calculation logic based on country
        if employee.country == "India":
            deduction = gross * 0.10  # 10% for India
        elif employee.country == "United States":
            deduction = gross * 0.12  # 12% for USA
        else:
            deduction = 0  # No deduction for other countries

        net_salary = gross - deduction
        return {
            "employee_id": employee.id,
            "gross_salary": gross,
            "deduction": deduction,
            "net_salary": net_salary
        }
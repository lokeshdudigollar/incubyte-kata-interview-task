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
    
    def update_employee(self, employee_id: int, **data):
        employee = self.repo.update_employee(employee_id, **data)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        return employee
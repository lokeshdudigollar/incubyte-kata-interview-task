from fastapi import HTTPException
from app.repositories.employee_repository import EmployeeRepository
from app.schema.salary_schema import SalaryResponse


class SalaryService:
    def __init__(self, repo: EmployeeRepository):
        self.repo = repo

    def _get_deduction_rate(self, country: str) -> float:
        """
        Get the deduction rate based on the employee's country.        
        """
        if country == "India":
            return 0.10
        elif country == "United States":
            return 0.12
        return 0
    
    def calculate_salary(self, employee_id: int):
        """
        Calculate salary breakdown for a given employee.

        Applies country-specific deduction rules:
        - India: 10% TDS
        - United States: 12% TDS
        - Others: No deduction

        Raises:
            HTTPException: If employee is not found.
        """
        employee = self.repo.get_employee(employee_id)

        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")

        gross_salary = employee.salary
        deduction_rate = self._get_deduction_rate(employee.country)
        deduction = int(gross_salary * deduction_rate)

        net_salary = gross_salary - deduction

        return SalaryResponse(
            employee_id=employee.id,
            gross_salary=gross_salary,
            deduction=deduction,
            net_salary=net_salary
        )
from sqlalchemy.orm import Session
from app.models import Employee
from sqlalchemy import func


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def _query(self):
        return self.db.query(Employee)

    def create_employee(self, full_name, job_title, country, salary):
        employee = Employee(
            full_name=full_name,
            job_title=job_title,
            country=country,
            salary=salary
        )

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee

    def get_employee(self, employee_id: int):
        return self.db.query(Employee).filter(Employee.id == employee_id).first()
    
    def update_employee(self, employee_id: int, **kwargs):
        employee = self.get_employee(employee_id)

        if not employee:
            return None

        for key, value in kwargs.items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)

        return employee
    
    def delete_employee(self, employee_id: int):
        employee = self.get_employee(employee_id)

        if not employee:
            return False

        self.db.delete(employee)
        self.db.commit()

        return True
    
    def get_salary_metrics_by_country(self, country: str):
        return (
            self.db.query(
                func.min(Employee.salary),
                func.max(Employee.salary),
                func.avg(Employee.salary)
            )
            .filter(Employee.country == country)
            .first()
        )
    
    def get_average_salary_by_job_title(self, job_title: str):
        return (
            self.db.query(func.avg(Employee.salary))
            .filter(Employee.job_title == job_title)
            .scalar()
        )
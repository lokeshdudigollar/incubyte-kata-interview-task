from sqlalchemy.orm import Session
from app.models import Employee


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
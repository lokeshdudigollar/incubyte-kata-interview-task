from sqlalchemy.orm import Session
from app.models import Employee
from sqlalchemy import func


class EmployeeRepository:

    def __init__(self, db: Session):
        self.db = db

    def _query(self):
        return self.db.query(Employee)

    def create_employee(self, full_name, job_title, country, salary) -> Employee:
        employee = Employee(
            full_name=full_name, job_title=job_title, country=country, salary=salary
        )

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)

        return employee

    def get_employee(self, employee_id: int) -> Employee | None:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def get_all_employees(self) -> list[Employee]:
        return self.db.query(Employee).order_by(Employee.id).all()

    def update_employee(self, employee_id: int, **kwargs) -> Employee | None:
        employee = self.get_employee(employee_id)

        if not employee:
            return None

        for key, value in kwargs.items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)

        return employee

    def delete_employee(self, employee_id: int) -> bool:
        employee = self.get_employee(employee_id)

        if not employee:
            return False

        self.db.delete(employee)
        self.db.commit()

        return True

    def get_salary_metrics_by_country(
        self, country: str
    ) -> tuple[float | None, float | None, float | None]:
        """
        Fetch aggregated salary metrics (min, max, avg) for a country.

        Returns a tuple of (min, max, avg). If no records exist,
        values will be (None, None, None).
        """
        search_term = country.lower().strip()

        # Define the alias group
        usa_aliases = ["usa", "united states"]
        if search_term in usa_aliases:
            # If the user searches for EITHER, we look for BOTH in the DB
            filter_condition = func.lower(Employee.country).in_(usa_aliases)
        else:
            # Standard case-insensitive match for other countries
            filter_condition = func.lower(Employee.country) == search_term

        return (
            self.db.query(
                func.min(Employee.salary),
                func.max(Employee.salary),
                func.avg(Employee.salary),
            )
            .filter(filter_condition)
            .first()
        )

    def get_average_salary_by_job_title(self, job_title: str) -> float | None:
        search_term = job_title.lower().strip()
        return (
            self.db.query(func.avg(Employee.salary))
            .filter(func.lower(Employee.job_title) == search_term)
            .scalar()
        )

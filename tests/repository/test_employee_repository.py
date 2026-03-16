from app.models import Employee
from app.repositories.employee_repository import EmployeeRepository


def test_create_employee(db_session):
    repo = EmployeeRepository(db_session)

    employee = repo.create_employee(
        full_name="Lokesh Dudigollar",
        job_title="Software Engineer",
        country="India",
        salary=300000
    )

    assert employee.id is not None
    assert employee.full_name == "Lokesh Dudigollar"
    assert employee.job_title == "Software Engineer"
    assert employee.country == "India"
    assert employee.salary == 300000

def test_get_employee_by_id(db_session):
    repo = EmployeeRepository(db_session)

    employee = repo.create_employee(
        full_name="Lokesh Dudigollar",
        job_title="Software Engineer",
        country="India",
        salary=300000
    )

    fetched = repo.get_employee(employee.id)

    assert fetched.id == employee.id
    assert fetched.full_name == "Lokesh Dudigollar"
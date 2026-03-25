from app.repositories.employee_repository import EmployeeRepository
from tests.utils.employee_data import employee_data


def test_create_employee(db_session):
    repo = EmployeeRepository(db_session)
    data = employee_data()
    employee = repo.create_employee(**data)

    assert employee.id is not None
    assert employee.full_name == data["full_name"]
    assert employee.job_title == data["job_title"]
    assert employee.country == data["country"]
    assert employee.salary == data["salary"]

def test_get_employee_by_id(db_session):
    repo = EmployeeRepository(db_session)

    employeeeCreated = repo.create_employee(**employee_data())

    employeeFetched = repo.get_employee(employeeeCreated.id)
    assert employeeFetched is not None
    assert employeeFetched.id == employeeeCreated.id
    assert employeeFetched.full_name == employeeeCreated.full_name

def test_get_all_employees(db_session):
    repo = EmployeeRepository(db_session)

    data1 = employee_data(full_name="A")
    data2 = employee_data(full_name="B")

    repo.create_employee(**data1)
    repo.create_employee(**data2)

    employees = repo.get_all_employees()

    assert len(employees) == 2
    assert employees[0].full_name == "A"
    assert employees[1].full_name == "B"
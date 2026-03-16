import pytest
from app.models.employee import Employee


def test_create_employee(db_session):
    employee = Employee(
        full_name="Lokesh Dudigollar",
        job_title="Software Engineer",
        country="India",
        salary=300000
    )

    db_session.add(employee)
    db_session.commit()

    assert employee.id is not None
    assert employee.full_name == "Lokesh Dudigollar"
    assert employee.job_title == "Software Engineer"
    assert employee.country == "India"
    assert employee.salary == 300000
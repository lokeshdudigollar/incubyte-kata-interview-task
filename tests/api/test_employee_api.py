from tests.utils.employee_data import employee_data
import pytest

# --- CREATE EMPLOYEE ---
def test_create_employee_api(client):
    data = employee_data()

    response = client.post("/employees", json=data)

    assert response.status_code == 201

    body = response.json()

    assert body["id"] is not None
    assert body["full_name"] == data["full_name"]
    assert body["job_title"] == data["job_title"]
    assert body["country"] == data["country"]
    assert body["salary"] == data["salary"]

# --- GET EMPLOYEE BY ID---

def test_get_employee_by_id_api(client):
    data = employee_data()

    # First create employee
    create_response = client.post("/employees", json=data)
    created = create_response.json()

    employee_id = created["id"]

    # Now fetch it
    response = client.get(f"/employees/{employee_id}")

    assert response.status_code == 200

    body = response.json()

    assert body["id"] == employee_id
    assert body["full_name"] == data["full_name"]
    assert body["job_title"] == data["job_title"]
    assert body["country"] == data["country"]
    assert body["salary"] == data["salary"]

# --- GET ALL EMPLOYEES---
def test_get_all_employees_api(client):
    # Create two distinct employees
    client.post("/employees", json=employee_data(full_name="Alice", salary=50000))
    client.post("/employees", json=employee_data(full_name="Bob", salary=60000))

    # Hit the GET collection endpoint
    response = client.get("/employees")

    # Assertions
    assert response.status_code == 200
    body = response.json()
    
    assert isinstance(body, list)
    assert len(body) >= 2
    
    # Ensure our specific test data is present
    names = [emp["full_name"] for emp in body]
    assert "Alice" in names
    assert "Bob" in names


# --- GET EMPLOYEE NOT FOUND ---
def test_get_employee_not_found(client):
    response = client.get("/employees/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

# Using parametrization to cover India (case-insensitive), USA (alias), and Defaults
@pytest.mark.parametrize("country_input, salary, expected_deduction, expected_net", [
    # India rule: 10% (Testing case sensitivity)
    ("India", 100000, 10000, 90000),
    ("india", 100000, 10000, 90000),
    ("INDIA", 100000, 10000, 90000),
    
    # US rule: 12% (Testing aliases and case)
    ("United States", 100000, 12000, 88000),
    ("USA", 100000, 12000, 88000),
    
    # Other countries: 0%
    ("Germany", 100000, 0, 100000),
    ("Brazil", 200000, 0, 200000)
])

def test_salary_calculation(client, country_input, salary, expected_deduction, expected_net):
    data = employee_data(country=country_input, salary=salary)

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")

    assert response.status_code == 200

    body = response.json()

    assert body["gross_salary"] == salary
    assert body["deduction"] == expected_deduction
    assert body["net_salary"] == expected_net


def test_salary_calculation_employee_not_found(client):
    response = client.get("/employees/9999/salary")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

def test_salary_metrics_by_country(client):
    # Create employees in different countries
    client.post("/employees", json=employee_data(country="India", salary=100000))
    client.post("/employees", json=employee_data(country="United States", salary=100000))
    client.post("/employees", json=employee_data(country="Germany", salary=100000))

    # Fetch salary for each employee and assert deductions
    response = client.get("/metrics/country/India")

    assert response.status_code == 200
    body = response.json()

    assert body["country"] == "India"
    assert body["min_salary"] == 100000
    assert body["max_salary"] == 100000
    assert body["average_salary"] == 100000

def test_salary_metrics_by_job_title(client):
    client.post("/employees", json=employee_data(job_title="Developer", salary=100000))
    client.post("/employees", json=employee_data(job_title="Developer", salary=150000))

    # Fetch salary for job title and assert deductions
    response = client.get("/metrics/job-title/Developer")

    assert response.status_code == 200
    body = response.json()

    assert body["job_title"] == "Developer"
    assert body["average_salary"] == 125000


def test_salary_metrics_nonexistent_country(client):
    # Fetch salary for each employee and assert deductions
    response = client.get("/metrics/country/Wakanda")

    assert response.status_code == 200
    body = response.json()

    assert body["country"] == "Wakanda"
    assert body["min_salary"] is None
    assert body["max_salary"] is None
    assert body["average_salary"] is None

def test_update_employee(client):
    data = employee_data()

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    updated_data = {
        "full_name": "Updated Name",
        "job_title": "Senior Engineer",
        "country": "India",
        "salary": 500000
    }

    response = client.put(f"/employees/{employee_id}", json=updated_data)

    assert response.status_code == 200
    body = response.json()

    assert body["full_name"] == "Updated Name"
    assert body["salary"] == 500000

def test_delete_employee(client):
    data = employee_data()

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 204

    # verify deletion
    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404
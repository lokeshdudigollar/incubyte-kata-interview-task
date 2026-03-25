from tests.utils.employee_data import employee_data
import pytest

# --- SALARY METRICS BY COUNTRY ---
@pytest.mark.parametrize("country_input", [
    "India",
    "india",
    "INDIA",
])
def test_salary_metrics_by_country(client, country_input):
    # Create employees in different countries
    client.post("/employees", json=employee_data(country="India", salary=100000))
    client.post("/employees", json=employee_data(country="United States", salary=100000))
    client.post("/employees", json=employee_data(country="Germany", salary=100000))

    # Fetch salary for each employee and assert deductions
    response = client.get(f"/metrics/country/{country_input}")

    assert response.status_code == 200
    body = response.json()

    assert body["country"] == country_input
    assert body["min_salary"] == 100000
    assert body["max_salary"] == 100000
    assert body["average_salary"] == 100000


# --- SALARY METRICS BY JOB TITLE ---
@pytest.mark.parametrize("job_title_input", [
    "Developer",
    "developer",
    "DEVELOPER",
])
def test_salary_metrics_by_job_title(client, job_title_input):
    client.post("/employees", json=employee_data(job_title="Developer", salary=100000))
    client.post("/employees", json=employee_data(job_title="Developer", salary=150000))

    # Fetch salary for job title and assert deductions
    response = client.get(f"/metrics/job-title/{job_title_input}")

    assert response.status_code == 200
    body = response.json()

    assert body["job_title"] == job_title_input
    assert body["average_salary"] == 125000

# --- SALARY METRICS FOR NON EXISTENT COUNTRY ---
def test_salary_metrics_nonexistent_country(client):
    # Fetch salary for each employee and assert deductions
    response = client.get("/metrics/country/Wakanda")

    assert response.status_code == 200
    body = response.json()

    assert body["country"] == "Wakanda"
    assert body["min_salary"] is None
    assert body["max_salary"] is None
    assert body["average_salary"] is None

# --- SALARY METRICS FOR NON EXISTENT JOB TITLE ---
def test_salary_metrics_nonexistent_job_title(client):
    # Fetch salary for each employee and assert deductions
    response = client.get("/metrics/job-title/notKnown")

    assert response.status_code == 200
    body = response.json()

    assert body["job_title"] == "notKnown"
    assert body["average_salary"] is None
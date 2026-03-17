from tests.utils.employee_data import employee_data

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


# --- GET EMPLOYEE NOT FOUND ---
def test_get_employee_not_found(client):
    response = client.get("/employees/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

def test_salary_calculation_india(client):
    data = employee_data(country="India", salary=100000)

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")

    assert response.status_code == 200

    body = response.json()

    assert body["employee_id"] == employee_id
    assert body["gross_salary"] == 100000
    assert body["deduction"] == 10000  # 10%
    assert body["net_salary"] == 90000

def test_salary_calculation_us(client):
    data = employee_data(country="United States", salary=100000)

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")

    assert response.status_code == 200

    body = response.json()

    assert body["employee_id"] == employee_id
    assert body["gross_salary"] == 100000
    assert body["deduction"] == 12000  # 12%
    assert body["net_salary"] == 88000

def test_salary_calculation_other_country(client):
    data = employee_data(country="Germany", salary=100000)

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")

    assert response.status_code == 200

    body = response.json()

    assert body["employee_id"] == employee_id
    assert body["gross_salary"] == 100000
    assert body["deduction"] == 0
    assert body["net_salary"] == 100000

def test_salary_calculation_employee_not_found(client):
    response = client.get("/employees/9999/salary")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"
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
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


# --- UPDATE EMPLOYEE ---
def test_update_employee(client):
    data = employee_data()

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    updated_data = {
        "full_name": "Updated Name",
        "job_title": "Senior Engineer",
        "country": "India",
        "salary": 500000,
    }

    response = client.put(f"/employees/{employee_id}", json=updated_data)

    assert response.status_code == 200
    body = response.json()

    assert body["full_name"] == "Updated Name"
    assert body["salary"] == 500000


# --- DELETE EMPLOYEE ---
def test_delete_employee(client):
    data = employee_data()

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.delete(f"/employees/{employee_id}")

    assert response.status_code == 204

    # verify deletion
    get_response = client.get(f"/employees/{employee_id}")
    assert get_response.status_code == 404


# --- CREATE EMPLOYEE MISSING FIELDS ---
def test_create_employee_missing_fields(client):
    data = employee_data()
    del data["full_name"]  # Remove a required field

    response = client.post("/employees", json=data)

    assert response.status_code == 422


# --- UPDATE EMPLOYEE NOT FOUND ---
def test_update_employee_not_found(client):
    updated_data = employee_data(full_name="Ghost", salary=99999)

    response = client.put("/employees/9999", json=updated_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


# --- DELETE EMPLOYEE NOT FOUND ---
def test_delete_employee_not_found(client):
    response = client.delete("/employees/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

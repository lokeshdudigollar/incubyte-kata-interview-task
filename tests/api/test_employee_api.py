from tests.utils.employee_data import employee_data


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
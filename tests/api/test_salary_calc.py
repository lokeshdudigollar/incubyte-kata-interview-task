from tests.utils.employee_data import employee_data
import pytest


# Using parametrization to cover India (case-insensitive), USA (alias), and Defaults
@pytest.mark.parametrize(
    "country_input, salary, expected_deduction, expected_net",
    [
        # India rule: 10% (Testing case sensitivity)
        ("India", 100000, 10000, 90000),
        ("india", 100000, 10000, 90000),
        ("INDIA", 100000, 10000, 90000),
        # US rule: 12% (Testing aliases and case)
        ("United States", 100000, 12000, 88000),
        ("USA", 100000, 12000, 88000),
        # Other countries: 0%
        ("Germany", 100000, 0, 100000),
        ("Brazil", 200000, 0, 200000),
    ],
)

# --- SALARY CALCULATION ---
def test_salary_calculation(
    client, country_input, salary, expected_deduction, expected_net
):
    data = employee_data(country=country_input, salary=salary)

    create_response = client.post("/employees", json=data)
    employee_id = create_response.json()["id"]

    response = client.get(f"/employees/{employee_id}/salary")

    assert response.status_code == 200

    body = response.json()

    assert body["gross_salary"] == salary
    assert body["deduction"] == expected_deduction
    assert body["net_salary"] == expected_net


# --- SALARY CALCULATION FOR NON EXISTENT EMPLOYEE ---
def test_salary_calculation_employee_not_found(client):
    response = client.get("/employees/9999/salary")

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"

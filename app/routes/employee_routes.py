from fastapi import APIRouter, Depends, Response, status
from app.schema.employee_schema import EmployeeCreate, EmployeeResponse
from app.dependencies import get_employee_service, get_salary_metrics_service, get_salary_service
from app.schema.salary_metrics_schema import (
    SalaryMetricsByCountryResponse, 
    SalaryMetricsByJobTitleResponse
)
from app.schema.salary_schema import SalaryResponse
from app.services.employee_service import EmployeeService
from app.services.salary_metrics_service import SalaryMetricsService
from app.services.salary_service import SalaryService

router = APIRouter()

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    return service.create_employee(**employee.model_dump())

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, service: EmployeeService = Depends(get_employee_service)):
    return service.get_employee(employee_id)

@router.get("/employees", response_model=list[EmployeeResponse])
def get_all_employees(service: EmployeeService = Depends(get_employee_service)):
    return service.get_all_employees()

@router.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, employee: EmployeeCreate, service: EmployeeService = Depends(get_employee_service)):
    return service.update_employee(
        employee_id,
        **employee.model_dump()
    )

@router.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, service: EmployeeService = Depends(get_employee_service)):
    service.delete_employee(employee_id)
    return Response(status_code=204)

@router.get("/employees/{employee_id}/salary", response_model=SalaryResponse)
def get_salary(employee_id: int, service: SalaryService = Depends(get_salary_service)):
    return service.calculate_salary(employee_id)

@router.get("/metrics/country/{country}", response_model=SalaryMetricsByCountryResponse)
def get_salary_metrics_by_country(country: str, service: SalaryMetricsService = Depends(get_salary_metrics_service)):
    return service.get_salary_metrics_by_country(country)

@router.get("/metrics/job-title/{job_title}", response_model=SalaryMetricsByJobTitleResponse)
def get_salary_metrics_by_job_title(job_title: str, service: SalaryMetricsService = Depends(get_salary_metrics_service)):
    return service.get_salary_metrics_by_job_title(job_title)
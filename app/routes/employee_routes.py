from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories.employee_repository import EmployeeRepository
from app.schema.employee_schema import EmployeeCreate, EmployeeResponse
from app.dependencies import get_db
from app.schema.salary_metrics_schema import SalaryMetricsByCountryResponse, SalaryMetricsByJobTitleResponse
from app.schema.salary_schema import SalaryResponse
from app.services.employee_service import EmployeeService
from app.services.salary_metrics_service import SalaryMetricsService
from app.services.salary_service import SalaryService

router = APIRouter()

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    service = EmployeeService(repo)
    data = employee.model_dump()
    created_employee = service.create_employee(**data)

    return created_employee

@router.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    service = EmployeeService(repo)
    return service.get_employee(employee_id)

@router.get("/employees/{employee_id}/salary", response_model=SalaryResponse)
def get_salary(employee_id: int, db: Session = Depends(get_db)):
    service = SalaryService(EmployeeRepository(db))
    return service.calculate_salary(employee_id)

@router.get("/metrics/country/{country}", response_model=SalaryMetricsByCountryResponse)
def get_metrics_by_country(country: str, db: Session = Depends(get_db)):
    service = SalaryMetricsService(EmployeeRepository(db))
    return service.get_metrics_by_country(country)

@router.get("/metrics/job-title/{job_title}", response_model=SalaryMetricsByJobTitleResponse)
def get_metrics_by_job_title(job_title: str, db: Session = Depends(get_db)):
    service = SalaryMetricsService(EmployeeRepository(db))
    return service.get_average_by_job_title(job_title)
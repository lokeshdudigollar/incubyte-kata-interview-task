from app.database.connection import SessionLocal
from fastapi import Depends
from sqlalchemy.orm import Session
from app.repositories.employee_repository import EmployeeRepository
from app.services.employee_service import EmployeeService
from app.services.salary_service import SalaryService
from app.services.salary_metrics_service import SalaryMetricsService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency injection functions for FastAPI routes.
# These functions provide service instances, which can be injected into 
# route handlers using FastAPI's Depends system.
def get_employee_service(db: Session = Depends(get_db)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(db))

def get_salary_metrics_service(db: Session = Depends(get_db)) -> SalaryMetricsService: 
    return SalaryMetricsService(EmployeeRepository(db))

def get_salary_service(db: Session = Depends(get_db)) -> SalaryService:
    return SalaryService(EmployeeRepository(db))
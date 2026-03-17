from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories.employee_repository import EmployeeRepository
from app.schema.employee_schema import EmployeeCreate, EmployeeResponse
from app.dependencies import get_db
from app.services.employee_service import EmployeeService

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
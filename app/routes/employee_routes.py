from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal
from app.repositories.employee_repository import EmployeeRepository
from app.schema.employee_schema import EmployeeCreate, EmployeeResponse

router = APIRouter()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    repo = EmployeeRepository(db)
    created_employee = repo.create_employee(
        full_name=employee.full_name,
        job_title=employee.job_title,
        country=employee.country,
        salary=employee.salary
    )

    return created_employee
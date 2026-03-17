# Incubyte Salary Management Kata

This project is a RESTful API for managing employee data and performing salary-related operations. It supports employee CRUD operations, salary calculation based on country-specific rules, and salary metrics aggregation.

The application is built using FastAPI, SQLAlchemy, and SQLite, following a layered architecture with Test-Driven Development (TDD).

### Tech Stack
Backend: FastAPI
ORM: SQLAlchemy
Database: SQLite
Testing: Pytest
Language: Python 3

### Tools used
Gemini, Anti gravity, Google search

## Employee CRUD
Create employee
Get employee by ID
Update employee
Delete employee

## Salary Calculation
Calculates deduction and net salary based on country specific TDS:
India > 10%
United States > 12%
Others > 0%

## Salary Metrics

### By country:
Minimum salary
Maximum salary
Average salary

### By job title:
Average salary

## API endpoints

### Employee:
POST /employees
GET /employees/{id}
PUT /employees/{id}
DELETE /employees/{id}

### Salary
GET /employees/{id}/salary

### Metrics
GET /metrics/country/{country}
GET /metrics/job-title/{job_title}

## Architechute responsibilities
Routes: Handle HTTP request/response
Services: Contain business logic (salary rules, metrics)
Repositories: Handle DB queries using SQLAlchemy
Schemas: Define API contracts using Pydantic

This separation ensures maintainability, testability, and scalability.

## Implementation Details (AI Usage)
AI tools (primarily Antigravity) were used intentionally to accelerate development while maintaining code quality and architectural control.

### How AI was used
Scaffolding & Boilerplate:
Generated initial structure for FastAPI routes, SQLAlchemy setup, and test scaffolding. This reduced time spent on repititive task where logic not required while I maintained decision behind placement of each file. Getting help from AI for writing conftest was super helpful here speifically db overriding of dependency 

Test Case design:
Most of the test cases were completely written using AI while I just made sure it considers it considers all required cases and also most impotantly made sure it doesn't leave edge cases where required

Refactoring:
While most logic was driven my understand of real-world projects AI helped me to keeps things structured and specifically helped moving logic to service layers. Ensured AI helped me to have SOLID(specifically the "S") and Dependency injection implemeted while refactoring the code

Debugging & Issue Resolution:
I think this is where AI was a lot more useful and time saving in many ways. It helped to find otu route path mismatches, DB connection issues, FAST API dependency overrides in tests, fitering pytest warnings,
import errors.


Document and Docstring:
This was mostly done by AI and then quick scan done manually

### How AI was NOT used

Core business logic decisions (e.g., salary rules, architecture design) were consciously reviewed and refined.
Final implementation choices were validated manually to ensure correctness and consistency.
AT times it would simply suggest unnecessary changes or lose context but with right counters made sure requiremts are met by it.
All generated code was reviewed, adapted, and integrated to align with clean architecture and TDD practices.

## How to run
1. Setup
pip install -r requirements.txt
2. Run Server
uvicorn app.main:app --reload
3. Run Tests
pytest



## Future Improvements[if required]

Add pagination for employee listing
Introduce validation for country via enums
Add authentication/authorization
Support partial updates (PATCH)
Add caching for metrics endpoints


## commit history
test: add failing test for employee model
feat: implement employee SQLAlchemy model
refactor: improve model imports

test: add failing test for employee repository
feat: implement employee repository
refactor: simplify repository queries

test: add failing test for create employee API
feat: implement POST /employees endpoint
refactor: moved get_db dependency to new folder for better injection
introduced employee service layer for separation of business logic concerns


test: add failing test for get employee API
feat: implement GET /employees/{id} endpoint


test: add failing test for employee salary endpoints
feat: implement salary endpoints
refactor: extract salary logic into salary service


test: add failing tests for salary metrics endpoint
feat: implement salary metrics endpoints
refactor: Added required validations

test: add failing tests for update employee endpoint
feat: implement PUT/employee endpoint

test: add failing tests for deleting employee record
feat: implement DELETE/employee endpoint

refactor: improve code structure and add validations

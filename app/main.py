from fastapi import FastAPI
from app.routes.employee_routes import router as employee_router

app = FastAPI()
app.include_router(employee_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
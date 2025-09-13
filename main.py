from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from .models import Employee, EmployeeUpdate
from . import crud
from typing import List, Dict,Union
from .models import AvgSalaryResponse

app = FastAPI(title="Employees API")

@app.get("/employees/avg-salary", response_model=List[AvgSalaryResponse])
def avg_salary():
    return crud.avg_salary_by_dept()

from .models import Employee

@app.get("/employees/search", response_model=List[Employee])
def search(skill: str, page: int = 1, per_page: int = 0):
    skip = 0
    limit = 0
    if per_page > 0:
        skip = (page - 1) * per_page
        limit = per_page
    return crud.search_by_skill(skill, skip=skip, limit=limit)


@app.post("/employees", response_model=Employee)
def create_employee(emp: Employee):
    payload = emp.dict()
    created = crud.create_employee(payload)
    if not created:
        raise HTTPException(status_code=400, detail="employee_id must be unique")
    return created

@app.get("/employees/{employee_id}", response_model=Employee)
def get_employee(employee_id: str):
    emp = crud.get_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{employee_id}", response_model=Employee)
def update_employee(employee_id: str, update: EmployeeUpdate):
    data = {k: v for k, v in update.dict().items() if v is not None}
    updated = crud.update_employee(employee_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: str):
    ok = crud.delete_employee(employee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}

@app.get("/employees")
def list_employees(
    department: Optional[str] = Query(None, description="Department filter"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    per_page: int = Query(0, ge=0, description="Items per page (0 = all)")
):
    # If department provided -> filter by department + sort by joining_date (newest first)
    skip = 0
    limit = 0
    if per_page > 0:
        skip = (page - 1) * per_page
        limit = per_page
    if department:
        return crud.list_employees_by_department(department)
    # If no department, return all (with pagination)
    # reuse Mongo find + sort
    from .database import employees_collection
    cursor = employees_collection.find().sort("joining_date", -1)
    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)
    return [ {k:v for k,v in doc.items() if k!="_id"} for doc in cursor ]








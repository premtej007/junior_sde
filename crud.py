from datetime import datetime, date

from typing import List, Optional, Dict, Any
from bson.objectid import ObjectId
from .database import employees_collection
import pymongo
from pymongo import DESCENDING

def _clean(doc: Dict[str, Any]) -> Dict[str, Any]:
    if not doc:
        return {}
    doc.pop("_id", None)
    return doc
def _normalize_dates(doc: dict) -> dict:
    """Convert datetime.date to datetime.datetime for MongoDB."""
    for k, v in doc.items():
        if isinstance(v, date) and not isinstance(v, datetime):
            doc[k] = datetime.combine(v, datetime.min.time())
    return doc

def create_employee(emp: dict):
    emp = _normalize_dates(emp.copy())
    try:
        employees_collection.insert_one(emp)
        return {k: v for k, v in emp.items() if k != "_id"}
    except pymongo.errors.DuplicateKeyError:
        return None
def get_employee(emp_id: str) -> Optional[Dict[str, Any]]:
    doc = employees_collection.find_one({"employee_id": emp_id})
    return _clean(doc) if doc else None
def update_employee(emp_id: str, data: dict):
    data = _normalize_dates(data.copy())
    if not data:
        return get_employee(emp_id)
    res = employees_collection.update_one({"employee_id": emp_id}, {"$set": data})
    if res.matched_count == 0:
        return None
    return get_employee(emp_id)






def delete_employee(emp_id: str) -> bool:
    res = employees_collection.delete_one({"employee_id": emp_id})
    return res.deleted_count > 0




def list_employees_by_department(department: str, skip: int = 0, limit: int = 0):
    cursor = employees_collection.find(
        {"department": department}
    ).sort("joining_date", DESCENDING)
    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)
    return [{k: v for k, v in doc.items() if k != "_id"} for doc in cursor]



def avg_salary_by_dept() -> List[Dict]:
    pipeline = [
        {
            "$group": {
                "_id": "$department",
                "avg_salary": {"$avg": "$salary"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "department": "$_id",
                # round to 2 decimal places
                "avg_salary": {"$round": ["$avg_salary", 2]}
            }
        }
    ]
    results = list(employees_collection.aggregate(pipeline))
    # ensure float values for avg_salary
    for r in results:
        if isinstance(r["avg_salary"], (int, float)):
            r["avg_salary"] = float(r["avg_salary"])
    return results

def search_by_skill(skill: str, skip: int = 0, limit: int = 0) -> List[Dict]:
    cursor = employees_collection.find(
        {"skills": skill}  # matches employees having the skill in skills array
    ).sort("joining_date", -1)

    if skip:
        cursor = cursor.skip(skip)
    if limit:
        cursor = cursor.limit(limit)

    return [_clean(doc) for doc in cursor]


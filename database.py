from pymongo import MongoClient, ASCENDING
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)

DB_NAME = "assessment_db"
db = client[DB_NAME]
employees_collection = db["employees"]

# Create index on employee_id for uniqueness (idempotent)
try:
    employees_collection.create_index([("employee_id", ASCENDING)], unique=True)
except Exception:
    # index creation may fail if already exists; ignore
    pass

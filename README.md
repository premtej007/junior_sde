# junior_sde
# Python + MongoDB Assessment – Employee Management API

A REST API built with **FastAPI** and **MongoDB** to manage employee data.

---

## 1️⃣  Prerequisites

* **Python 3.10+** (or any recent 3.x)
* **MongoDB** running locally  
  *Database name:* `assessment_db`  
  *Collection name:* `employees`

---

## 2️⃣  Project Setup

### Clone / Download
Place the project folder (e.g. `junior_sde`) on your machine.

### Create and Activate a Virtual Environment
```bash
cd junior_sde
python -m venv venv
# Windows PowerShell
venv\Scripts\activate


# macOS / Linux
source venv/bin/activate
Install Dependencies
pip install -r requirements.txt

```

Configure MongoDB (Default)

The app expects a local Mongo instance:

mongodb://localhost:27017/assessement_db




3️⃣ Run the API

From the project root:

uvicorn main:app --reload


FastAPI will start at:

http://127.0.0.1:8000


Interactive documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

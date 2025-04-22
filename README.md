# 🚀 Talent Recruiter

A scalable, modular microservice built with **FastAPI**, **SQLAlchemy**, and **MySQL** — designed for real-world enterprise-grade backend applications.

# Contributors:
**Rakesh Shekhawat**, 
**Anshul Pareek**, 
**Pankaj Kumar**
---

## 🗂️ Project Structure
project/ │ 
├── app/ │ 
├── main.py # Entry point for FastAPI app │ 
├── database/ │ 
│ └── mysqlConnection.py # SQLAlchemy DB connection │ 
├── entities/ │ 
│ └── user.py # msyql schema and model for the queries │ 
├── users/ │ #Individual modules
│ ├── model.py # SQLAlchemy models │ 
│ ├── service.py # Business logic │ 
│ |── controller.py # API routes │ 
├── .env # Environment variables
├── requirements.txt # Python dependencies 
└── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo

**2. Create & Activate Virtual Environment**
--python -m .venv venv
--source venv/bin/activate   # macOS/Linux
--venv\Scripts\activate      # Windows

**3. Install Requirements**
--pip install -r requirements.txt

**4. Setup .env file**
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/dbname

**5. Run the App**
uvicorn app.main:app --reload

**API Testing**
Once running, access the auto-generated docs at:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

**Technologies Used**
-Python 3.10+
-FastAPI
-SQLAlchemy 2.x
-Pydantic
-MySQL
-Uvicorn

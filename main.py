from fastapi import FastAPI, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from typing import List

from database import SessionLocal, engine, Base
from models import Employee

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Excel Upload API Running"}


from typing import List

@app.post("/upload-excel")
async def upload_excel(files: List[UploadFile] = File(...)):
    return {
        "count": len(files),
        "files": [f.filename for f in files]
    }

    db: Session = SessionLocal()

    try:

        if not file.filename.endswith((".xlsx", ".xls")):
            raise HTTPException(
                status_code=400,
                detail="Only Excel files are allowed"
            )

        df = pd.read_excel(file.file)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        required_columns = [
            "name",
            "age",
            "department"
        ]

        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise HTTPException(
                status_code=400,
                detail=f"Missing columns: {missing_columns}"
            )

        if df.isnull().values.any():
            raise HTTPException(
                status_code=400,
                detail="Excel contains null values"
            )

        try:
            df["age"] = df["age"].astype(int)
        except:
            raise HTTPException(
                status_code=400,
                detail="Age column must contain integers only"
            )

        records_inserted = 0

        for _, row in df.iterrows():
            existing = db.query(Employee).filter(
        Employee.name == row["name"],
        Employee.age == int(row["age"]),
        Employee.department == row["department"]
        ).first()
            if existing:
                continue
            employee = Employee(
        name=row["name"],
        age=int(row["age"]),
        department=row["department"]
        )
            db.add(employee)
            
            total_records += 1

        db.commit()

        return {
            "message": "Excel uploaded successfully",
            "records_inserted": records_inserted
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:
        db.close()


@app.get("/employees")
def get_employees():

    db: Session = SessionLocal()

    try:

        employees = db.query(Employee).all()

        result = []

        for emp in employees:
            result.append({
                "id": emp.id,
                "name": emp.name,
                "age": emp.age,
                "department": emp.department
            })

        return result

    finally:
        db.close()
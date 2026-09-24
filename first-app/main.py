from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
import requests
import json

from database import SessionLocal, engine, Base
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(description="This is My First FastAPI App")


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to FastAPI"}


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "Database Connected Successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/product")
def get_product():
    response = requests.get("https://dummyjson.com/products")
    return response.json()



@app.get("/staff", response_model=List[schemas.StaffResponse])
def get_staff(db: Session = Depends(get_db)):
    staff = db.query(models.Staff).all()
    return staff



@app.get("/staff/{id}", response_model=schemas.StaffResponse)
def get_staff_by_id(id: int, db: Session = Depends(get_db)):
    staff = db.query(models.Staff).filter(models.Staff.id == id).first()

    if staff is None:
        raise HTTPException(status_code=404, detail="Staff Not Found")

    return staff


@app.post("/staff", response_model=schemas.StaffResponse)
def create_staff(staff: schemas.StaffCreate, db: Session = Depends(get_db)):
    new_staff = models.Staff(
        emp_name=staff.emp_name,
        emp_age=staff.emp_age,
        emp_city=staff.emp_city
    )

    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return new_staff



@app.post("/import-json")
def import_json(db: Session = Depends(get_db)):
    try:
        with open("staff.json", "r") as file:
            data = json.load(file)

        for item in data:
            staff = models.Staff(
                emp_name=item["emp_name"],
                emp_age=item["emp_age"],
                emp_city=item["emp_city"]
            )

            db.add(staff)

        db.commit()

        return {
            "message": "JSON data inserted successfully",
            "total_records": len(data)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# @app.post("/users") 
# def post_users():
#     response = requests.get("https://dummyjson.com/users")
#     data = response.json()
#     return data


@app.delete("/staff/{id}")
def delete_staff(id: int, db: Session = Depends(get_db)):
    
    staff = db.query(models.Staff).filter(models.Staff.id == id).first()

    if staff is None:
        raise HTTPException(status_code=404,detail="Staff Not Found")

    db.delete(staff)
    db.commit()

    return {
        "message": "Staff deleted successfully"
    }



@app.delete("/staff")
def delete_all_staff(db: Session = Depends(get_db)):
    deleted = db.query(models.Staff).delete()

    db.commit()

    return {
        "message": "All staff records deleted successfully",
        "total_deleted": deleted
    }



@app.put("/staff/{id}", response_model=schemas.StaffResponse)
def update_staff(id: int,staff: schemas.StaffCreate,db: Session = Depends(get_db)):

    db_staff = db.query(models.Staff).filter(models.Staff.id == id).first()

    if db_staff is None:raise HTTPException(status_code=404,detail="Staff Not Found")

    db_staff.emp_name = staff.emp_name
    db_staff.emp_age = staff.emp_age
    db_staff.emp_city = staff.emp_city

    db.commit()
    db.refresh(db_staff)

    return db_staff
from pydantic import BaseModel

class StaffCreate(BaseModel):
    emp_name: str
    emp_age: int
    emp_city: str

class StaffResponse(BaseModel):
    id: int
    emp_name: str
    emp_age: int
    emp_city: str

    class Config:
        from_attributes = True
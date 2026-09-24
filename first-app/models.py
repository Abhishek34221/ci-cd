from sqlalchemy import Column,Integer ,String , Float
from database import Base

class Staff(Base):
    __tablename__="staff"
    id=Column(Integer,primary_key=True,index=True)
    emp_name=Column(String(100))
    emp_age=Column(Integer)
    emp_city=Column(String(100))
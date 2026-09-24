from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker , declarative_base
from urllib.parse import quote_plus
password=quote_plus("abhi@123")

DATABASE_URL=f"mysql+pymysql://root:{password}@localhost:3306/fast_api_db"

engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()
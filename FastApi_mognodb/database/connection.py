import os

from dotenv import load_dotenv
from mongoengine import connect


load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")


def connect_database():

    try:

        connect(
            db=MONGODB_DB,
            host=MONGODB_URI
        )

        print("MongoDB Connected Successfully ✅")
        print(f"Database: {MONGODB_DB}")

    except Exception as e:

        print("MongoDB Connection Failed ❌")
        print(e)
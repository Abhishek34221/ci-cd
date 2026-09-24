from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.connection import connect_database
from routes.auth import router as auth_router
from routes.get_user import router as user_router
from routes.destination import router as destination_router



connect_database()



app = FastAPI(
    title="Tour & Travel Services API",
    version="1.0.0"
)


# CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5000",
        "http://localhost:5000",

        # Agar Flask kisi aur port par chal raha ho
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(auth_router)
app.include_router(user_router)
app.include_router(destination_router)




@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "mongodb": "Connected"
    }
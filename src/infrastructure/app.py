from fastapi import FastAPI, Depends
from src.repositories.database.core import engine, Base
from src.infrastructure.routes import mahasiswa_router
from src.dependencies import get_mahasiswa_service # Import from the new dependencies file

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# The get_mahasiswa_service dependency is now imported from src.dependencies
app.include_router(mahasiswa_router, prefix="/mahasiswa", tags=["mahasiswa"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the P-ToDo-Y Mahasiswa API!"}

from fastapi import FastAPI

from src.infrastructure.routes import (
    dosen_router,
    jadwal_router,
    mahasiswa_router,
    mata_kuliah_router,
    tugas_router,
)
from src.repositories.database.core import Base, engine

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# The get_mahasiswa_service dependency is now imported from src.dependencies
app.include_router(mahasiswa_router, prefix="/mahasiswa", tags=["mahasiswa"])
app.include_router(mata_kuliah_router, prefix="/mata-kuliah", tags=["mata-kuliah"])
app.include_router(dosen_router, prefix="/dosen", tags=["dosen"])
app.include_router(jadwal_router, prefix="/jadwal", tags=["jadwal"])
app.include_router(tugas_router, prefix="/tugas", tags=["tugas"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the P-ToDo-Y Mahasiswa API!"}

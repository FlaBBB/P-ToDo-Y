from sqlalchemy.orm import Session
from fastapi import Depends
from src.repositories.database.core import get_db_session
from src.repositories.database.mahasiswa import MahasiswaRepository
from src.application.usecases.mahasiswa import MahasiswaService


def get_mahasiswa_service(db: Session = Depends(get_db_session)) -> MahasiswaService:
    repository = MahasiswaRepository(session_db=db)
    service = MahasiswaService(mahasiswa_repo=repository)
    return service
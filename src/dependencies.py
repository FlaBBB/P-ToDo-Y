from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.mahasiswa import MahasiswaService
from src.repositories.database.core import get_db_session
from src.repositories.database.mahasiswa import MahasiswaRepository


def get_mahasiswa_service(db: Session = Depends(get_db_session)) -> MahasiswaService:
    repository = MahasiswaRepository(session_db=db)
    service = MahasiswaService(mahasiswa_repo=repository)
    return service

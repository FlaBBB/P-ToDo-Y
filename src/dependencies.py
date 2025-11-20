from fastapi import Depends
from sqlalchemy.orm import Session

from src.application.usecases.mahasiswa import MahasiswaService
from src.repositories.database.core import get_db_session
from src.repositories.database.mahasiswa import MahasiswaRepository


def get_mahasiswa_service(db: Session = Depends(get_db_session)) -> MahasiswaService:
    repository = MahasiswaRepository(session_db=db)
    service = MahasiswaService(mahasiswa_repo=repository)
    return service


from src.application.usecases.mata_kuliah import MataKuliahService
from src.repositories.database.mata_kuliah import MataKuliahRepository


def get_mata_kuliah_service(db: Session = Depends(get_db_session)) -> MataKuliahService:
    repository = MataKuliahRepository(session_db=db)
    service = MataKuliahService(mata_kuliah_repo=repository)
    return service


from src.application.usecases.dosen import DosenService
from src.repositories.database.dosen import DosenRepository


def get_dosen_service(db: Session = Depends(get_db_session)) -> DosenService:
    repository = DosenRepository(session_db=db)
    service = DosenService(dosen_repo=repository)
    return service


from src.application.usecases.jadwal import JadwalService
from src.repositories.database.jadwal import JadwalRepository


def get_jadwal_service(db: Session = Depends(get_db_session)) -> JadwalService:
    repository = JadwalRepository(session_db=db)
    service = JadwalService(jadwal_repo=repository)
    return service


from src.application.usecases.tugas import TugasService
from src.repositories.database.tugas import TugasRepository


def get_tugas_service(db: Session = Depends(get_db_session)) -> TugasService:
    repository = TugasRepository(session_db=db)
    service = TugasService(tugas_repo=repository)
    return service

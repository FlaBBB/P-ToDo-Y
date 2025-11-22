from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel

class StatusTugas(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class CreateTugasDto(BaseModel):
    judul: str
    deskripsi: str
    deadline: datetime
    status: StatusTugas = StatusTugas.PENDING
    mata_kuliah_id: Optional[int] = None
    mahasiswa_id: Optional[int] = None

class UpdateTugasDto(BaseModel):
    id: int
    judul: str
    deskripsi: str
    deadline: datetime
    status: StatusTugas
    mata_kuliah_id: Optional[int] = None
    mahasiswa_id: Optional[int] = None

class TugasDto(BaseModel):
    id: int
    judul: str
    deskripsi: str
    deadline: datetime
    status: StatusTugas
    mata_kuliah_id: Optional[int] = None
    mahasiswa_id: Optional[int] = None

    class Config:
        from_attributes = True

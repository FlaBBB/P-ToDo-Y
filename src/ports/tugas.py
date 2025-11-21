from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from src.application.dtos.tugas_dto import StatusTugas


class GetTugasPort(BaseModel):
    id: Optional[int] = None
    judul: Optional[str] = None
    status: Optional[StatusTugas] = None
    mata_kuliah_id: Optional[int] = None
    mahasiswa_id: Optional[int] = None
    deadline_from: Optional[datetime] = None
    deadline_to: Optional[datetime] = None
    order_by: Optional[str] = None
    order: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None

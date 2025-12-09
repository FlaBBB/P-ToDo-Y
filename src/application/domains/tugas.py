from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.application.domains.base_entity import BaseEntity
from src.application.enums import StatusTugas


@dataclass
class Tugas(BaseEntity):
    judul: str
    deskripsi: str
    deadline: datetime
    status: StatusTugas
    mata_kuliah_id: Optional[int]
    mahasiswa_id: Optional[int]

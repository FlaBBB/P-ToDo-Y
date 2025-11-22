from datetime import time
from enum import Enum

from pydantic import BaseModel


class JadwalStatus(str, Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    DONE = "done"


class CreateJadwalDto(BaseModel):
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    status: JadwalStatus = JadwalStatus.SCHEDULED


class UpdateJadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    status: JadwalStatus


class JadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    status: JadwalStatus

    class Config:
        from_attributes = True

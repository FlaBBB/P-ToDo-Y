from datetime import time
from typing import Optional
from pydantic import BaseModel

class CreateJadwalDto(BaseModel):
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    is_active: bool = True

class UpdateJadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    is_active: bool

class JadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    is_active: bool

    class Config:
        from_attributes = True

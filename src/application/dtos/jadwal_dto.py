from datetime import time

from pydantic import BaseModel


class CreateJadwalDto(BaseModel):
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int


class UpdateJadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int


class JadwalDto(BaseModel):
    id: int
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int

    class Config:
        from_attributes = True

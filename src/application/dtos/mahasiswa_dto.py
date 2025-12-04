from datetime import date
from typing import Optional
from pydantic import BaseModel
from src.application.enums import MahasiswaStatus


class CreateMahasiswaDto(BaseModel):
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus = MahasiswaStatus.ACTIVE


class UpdateMahasiswaDto(BaseModel):
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus


class MahasiswaDto(BaseModel):
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus

    class Config:
        from_attributes = True

from typing import Optional
from pydantic import BaseModel


class CreateMataKuliahDto(BaseModel):
    kode_mk: str
    nama_mk: str
    sks: int


class UpdateMataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int


class MataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int

    class Config:
        from_attributes = True

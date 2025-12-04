from typing import Optional
from pydantic import BaseModel

class CreateMataKuliahDto(BaseModel):
    kode_mk: str
    nama_mk: str
    sks: int
    is_active: bool = True

class UpdateMataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int
    is_active: bool

class MataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int
    is_active: bool

    class Config:
        from_attributes = True

from enum import Enum

from pydantic import BaseModel


class MataKuliahStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CreateMataKuliahDto(BaseModel):
    kode_mk: str
    nama_mk: str
    sks: int
    status: MataKuliahStatus = MataKuliahStatus.ACTIVE


class UpdateMataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int
    status: MataKuliahStatus


class MataKuliahDto(BaseModel):
    id: int
    kode_mk: str
    nama_mk: str
    sks: int
    status: MataKuliahStatus

    class Config:
        from_attributes = True

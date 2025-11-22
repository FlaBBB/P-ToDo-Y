from enum import Enum

from pydantic import BaseModel, EmailStr


class DosenStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CreateDosenDto(BaseModel):
    nidn: str
    nama: str
    email: EmailStr
    status: DosenStatus = DosenStatus.ACTIVE


class UpdateDosenDto(BaseModel):
    id: int
    nidn: str
    nama: str
    email: EmailStr
    status: DosenStatus


class DosenDto(BaseModel):
    id: int
    nidn: str
    nama: str
    email: str
    status: DosenStatus

    class Config:
        from_attributes = True

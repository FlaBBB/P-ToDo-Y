from pydantic import BaseModel, EmailStr
from src.application.enums import DosenStatus


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
    email: EmailStr
    status: DosenStatus

    class Config:
        from_attributes = True

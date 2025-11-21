from typing import Optional
from pydantic import BaseModel, EmailStr


class CreateDosenDto(BaseModel):
    nidn: str
    nama: str
    email: EmailStr


class UpdateDosenDto(BaseModel):
    id: int
    nidn: str
    nama: str
    email: EmailStr


class DosenDto(BaseModel):
    id: int
    nidn: str
    nama: str
    email: str

    class Config:
        from_attributes = True

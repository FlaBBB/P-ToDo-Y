from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class CreateMahasiswaDto:
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date


@dataclass
class UpdateMahasiswaDto:
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date


@dataclass
class MahasiswaDto:
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date

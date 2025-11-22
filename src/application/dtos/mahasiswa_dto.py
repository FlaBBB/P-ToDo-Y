from dataclasses import dataclass
from datetime import date
from enum import Enum


class MahasiswaStatus(str, Enum):
    ACTIVE = "active"
    DO = "do"
    CUTI = "cuti"
    LULUS = "lulus"
    INACTIVE = "inactive"


@dataclass
class CreateMahasiswaDto:
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus = MahasiswaStatus.ACTIVE


@dataclass
class UpdateMahasiswaDto:
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus


@dataclass
class MahasiswaDto:
    id: int
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date
    status: MahasiswaStatus

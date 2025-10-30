from datetime import date
from src.application.domains.base_entity import BaseEntity
from dataclasses import dataclass


@dataclass
class Mahasiswa(BaseEntity):
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date

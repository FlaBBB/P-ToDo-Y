from dataclasses import dataclass
from datetime import date

from src.application.domains.base_entity import BaseEntity


@dataclass
class Mahasiswa(BaseEntity):
    nim: str
    nama: str
    kelas: str
    tempat_lahir: str
    tanggal_lahir: date

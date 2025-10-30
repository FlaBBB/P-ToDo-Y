from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.ports.get_base import GetBasePort


@dataclass
class GetMahasiswaPort(GetBasePort):
    id: Optional[int] = None
    nim: Optional[str] = None
    nama: Optional[str] = None
    kelas: Optional[str] = None
    tempat_lahir: Optional[str] = None
    tanggal_lahir: Optional[date] = None

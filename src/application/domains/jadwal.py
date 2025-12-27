from dataclasses import dataclass
from datetime import time
from src.application.domains.base_entity import BaseEntity


@dataclass
class Jadwal(BaseEntity):
    hari: str
    jam_mulai: time
    jam_selesai: time
    ruangan: str
    mata_kuliah_id: int
    dosen_id: int
    is_active: bool

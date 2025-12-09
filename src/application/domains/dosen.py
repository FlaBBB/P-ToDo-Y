from dataclasses import dataclass
from src.application.domains.base_entity import BaseEntity
from src.application.enums import DosenStatus


@dataclass
class Dosen(BaseEntity):
    nidn: str
    nama: str
    email: str
    status: DosenStatus

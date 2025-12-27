from dataclasses import dataclass
from src.application.domains.base_entity import BaseEntity


@dataclass
class MataKuliah(BaseEntity):
    kode_mk: str
    nama_mk: str
    sks: int
    is_active: bool

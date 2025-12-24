from datetime import time
from typing import Optional
from typing_extensions import override

from sqlalchemy import ForeignKey, Integer, String, Time, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.dtos.jadwal_dto import JadwalDto
from src.repositories.database.core import Base
from src.repositories.database.models.dosen import DosenModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


class JadwalModel(Base):
    __tablename__ = "jadwal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    hari: Mapped[str] = mapped_column(String(10), nullable=False)
    jam_mulai: Mapped[time] = mapped_column(Time, nullable=False)
    jam_selesai: Mapped[time] = mapped_column(Time, nullable=False)
    ruangan: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    mata_kuliah_id: Mapped[int] = mapped_column(Integer, ForeignKey("mata_kuliah.id"), nullable=False)
    dosen_id: Mapped[int] = mapped_column(Integer, ForeignKey("dosen.id"), nullable=False)

    mata_kuliah: Mapped[MataKuliahModel] = relationship("MataKuliahModel")
    dosen: Mapped[DosenModel] = relationship("DosenModel")

    @override
    def to_entity(self) -> JadwalDto:
        return JadwalDto(
            id=self.id,
            hari=self.hari,
            jam_mulai=self.jam_mulai,
            jam_selesai=self.jam_selesai,
            ruangan=self.ruangan,
            mata_kuliah_id=self.mata_kuliah_id,
            dosen_id=self.dosen_id,
            is_active=self.is_active,
        )

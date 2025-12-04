from datetime import datetime
from typing import Optional, override

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.application.dtos.tugas_dto import StatusTugas, TugasDto
from src.repositories.database.core import Base
from src.repositories.database.models.mahasiswa import MahasiswaModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


class TugasModel(Base):
    __tablename__ = "tugas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    judul: Mapped[str] = mapped_column(String(200), nullable=False)
    deskripsi: Mapped[str] = mapped_column(Text, nullable=True)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[StatusTugas] = mapped_column(
        Enum(StatusTugas), default=StatusTugas.PENDING
    )

    mata_kuliah_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("mata_kuliah.id"), nullable=True
    )
    mahasiswa_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("mahasiswa.id"), nullable=True
    )

    mata_kuliah: Mapped[Optional[MataKuliahModel]] = relationship("MataKuliahModel")
    mahasiswa: Mapped[Optional[MahasiswaModel]] = relationship("MahasiswaModel")

    @override
    def to_entity(self) -> TugasDto:
        return TugasDto(
            id=self.id,
            judul=self.judul,
            deskripsi=self.deskripsi,
            deadline=self.deadline,
            status=self.status,
            mata_kuliah_id=self.mata_kuliah_id,
            mahasiswa_id=self.mahasiswa_id,
        )

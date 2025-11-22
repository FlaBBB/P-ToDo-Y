from typing import override

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.application.dtos.mata_kuliah_dto import MataKuliahDto, MataKuliahStatus
from src.repositories.database.core import Base


class MataKuliahModel(Base):
    __tablename__ = "mata_kuliah"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    kode_mk: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nama_mk: Mapped[str] = mapped_column(String(100), nullable=False)
    nama_mk: Mapped[str] = mapped_column(String(100), nullable=False)
    sks: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[MataKuliahStatus] = mapped_column(
        Enum(MataKuliahStatus), default=MataKuliahStatus.ACTIVE
    )

    @override
    def to_entity(self) -> MataKuliahDto:
        return MataKuliahDto(
            id=self.id,
            kode_mk=self.kode_mk,
            nama_mk=self.nama_mk,
            sks=self.sks,
            status=self.status,
        )

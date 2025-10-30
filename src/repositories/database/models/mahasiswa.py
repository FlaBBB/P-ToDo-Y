from typing import override
from src.repositories.database.models.base import Base
from src.application.domains.mahasiswa import Mahasiswa
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from datetime import date


class MahasiswaModel(Base):
    __tablename__ = "mahasiswa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nim: Mapped[str] = mapped_column(String(10), nullable=False)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    kelas: Mapped[str] = mapped_column(String(10), nullable=False)
    tempat_lahir: Mapped[str] = mapped_column(String(100), nullable=False)
    tanggal_lahir: Mapped[date] = mapped_column(nullable=False)

    @override
    def to_entity(self) -> Mahasiswa:
        return Mahasiswa(
            nim=self.nim,
            nama=self.nama,
            kelas=self.kelas,
            tempat_lahir=self.tempat_lahir,
            tanggal_lahir=self.tanggal_lahir,
        )

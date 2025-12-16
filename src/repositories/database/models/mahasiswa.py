from datetime import date
from typing_extensions import override

from sqlalchemy import Date, Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.application.dtos.mahasiswa_dto import MahasiswaDto
from src.application.enums import MahasiswaStatus
from src.repositories.database.core import Base


class MahasiswaModel(Base):
    __tablename__ = "mahasiswa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nim: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    kelas: Mapped[str] = mapped_column(String(20), nullable=False)
    tempat_lahir: Mapped[str] = mapped_column(String(100), nullable=False)
    tanggal_lahir: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[MahasiswaStatus] = mapped_column(Enum(MahasiswaStatus), default=MahasiswaStatus.ACTIVE)

    @override
    def to_entity(self) -> MahasiswaDto:
        return MahasiswaDto(
            id=self.id,
            nim=self.nim,
            nama=self.nama,
            kelas=self.kelas,
            tempat_lahir=self.tempat_lahir,
            tanggal_lahir=self.tanggal_lahir,
            status=self.status,
        )

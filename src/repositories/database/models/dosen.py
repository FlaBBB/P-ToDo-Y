from typing_extensions import override

from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.application.dtos.dosen_dto import DosenDto
from src.application.enums import DosenStatus
from src.repositories.database.core import Base


class DosenModel(Base):
    __tablename__ = "dosen"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nidn: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nama: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    status: Mapped[DosenStatus] = mapped_column(Enum(DosenStatus), default=DosenStatus.ACTIVE)

    @override
    def to_entity(self) -> DosenDto:
        return DosenDto(
            id=self.id,
            nidn=self.nidn,
            nama=self.nama,
            email=self.email,
            status=self.status,
        )

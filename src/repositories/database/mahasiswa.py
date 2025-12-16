from typing import Optional
from typing_extensions import override

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.dtos.mahasiswa_dto import (
    CreateMahasiswaDto,
    MahasiswaDto,
    UpdateMahasiswaDto,
)
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.ports.mahasiswa import GetMahasiswaPort
from src.repositories.database.models.mahasiswa import MahasiswaModel


class MahasiswaRepository(MahasiswaRepositoryInterface):
    def __init__(self, session_db: Session):
        self.session: Session = session_db

    @override
    def create(self, mahasiswa_dto: CreateMahasiswaDto) -> MahasiswaDto:
        mahasiswa_model = MahasiswaModel(
            nim=mahasiswa_dto.nim,
            nama=mahasiswa_dto.nama,
            kelas=mahasiswa_dto.kelas,
            tempat_lahir=mahasiswa_dto.tempat_lahir,
            tanggal_lahir=mahasiswa_dto.tanggal_lahir,
            status=mahasiswa_dto.status,
        )
        self.session.add(mahasiswa_model)
        self.session.commit()
        self.session.refresh(mahasiswa_model)
        return MahasiswaDto(
            id=mahasiswa_model.id,
            nim=mahasiswa_model.nim,
            nama=mahasiswa_model.nama,
            kelas=mahasiswa_model.kelas,
            tempat_lahir=mahasiswa_model.tempat_lahir,
            tanggal_lahir=mahasiswa_model.tanggal_lahir,
            status=mahasiswa_model.status,
        )

    @override
    def read(self, get_mahasiswa_port: GetMahasiswaPort) -> list[MahasiswaDto]:
        stmt = select(MahasiswaModel)

        filters = []
        if get_mahasiswa_port.id:
            filters.append(MahasiswaModel.id == get_mahasiswa_port.id)
        if get_mahasiswa_port.nim:
            filters.append(MahasiswaModel.nim == get_mahasiswa_port.nim)
        if get_mahasiswa_port.nama:
            filters.append(MahasiswaModel.nama.ilike(f"%{get_mahasiswa_port.nama}%"))
        if get_mahasiswa_port.kelas:
            filters.append(MahasiswaModel.kelas == get_mahasiswa_port.kelas)
        if get_mahasiswa_port.tempat_lahir:
            filters.append(
                MahasiswaModel.tempat_lahir.ilike(
                    f"%{get_mahasiswa_port.tempat_lahir}%"
                )
            )
        if get_mahasiswa_port.tanggal_lahir:
            filters.append(
                MahasiswaModel.tanggal_lahir == get_mahasiswa_port.tanggal_lahir
            )

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_mahasiswa_port.order_by:
            order_column = getattr(MahasiswaModel, get_mahasiswa_port.order_by, None)
            if order_column:
                if (
                    get_mahasiswa_port.order
                    and get_mahasiswa_port.order.lower() == "desc"
                ):
                    stmt = stmt.order_by(order_column.desc())
                else:
                    stmt = stmt.order_by(order_column.asc())

        if get_mahasiswa_port.limit:
            stmt = stmt.limit(get_mahasiswa_port.limit)
        if get_mahasiswa_port.page and get_mahasiswa_port.limit:
            stmt = stmt.offset((get_mahasiswa_port.page - 1) * get_mahasiswa_port.limit)

        mahasiswa_models = self.session.execute(stmt).scalars().all()
        return [
            MahasiswaDto(
                id=m.id,
                nim=m.nim,
                nama=m.nama,
                kelas=m.kelas,
                tempat_lahir=m.tempat_lahir,
                tanggal_lahir=m.tanggal_lahir,
                status=m.status,
            )
            for m in mahasiswa_models
        ]

    @override
    def update(self, mahasiswa_dto: UpdateMahasiswaDto) -> MahasiswaDto:
        mahasiswa_model: Optional[MahasiswaModel] = self.session.get(
            MahasiswaModel, mahasiswa_dto.id
        )
        if not mahasiswa_model:
            raise NotFoundException(
                resource_name="Mahasiswa", identifier=mahasiswa_dto.id
            )

        mahasiswa_model.nim = mahasiswa_dto.nim
        mahasiswa_model.nama = mahasiswa_dto.nama
        mahasiswa_model.kelas = mahasiswa_dto.kelas
        mahasiswa_model.tempat_lahir = mahasiswa_dto.tempat_lahir
        mahasiswa_model.tanggal_lahir = mahasiswa_dto.tanggal_lahir
        mahasiswa_model.status = mahasiswa_dto.status

        self.session.add(mahasiswa_model)
        self.session.commit()
        self.session.refresh(mahasiswa_model)
        return MahasiswaDto(
            id=mahasiswa_model.id,
            nim=mahasiswa_model.nim,
            nama=mahasiswa_model.nama,
            kelas=mahasiswa_model.kelas,
            tempat_lahir=mahasiswa_model.tempat_lahir,
            tanggal_lahir=mahasiswa_model.tanggal_lahir,
            status=mahasiswa_model.status,
        )

    @override
    def delete(self, mahasiswa_id: int) -> bool:
        mahasiswa_model: Optional[MahasiswaModel] = self.session.get(
            MahasiswaModel, mahasiswa_id
        )
        if not mahasiswa_model:
            raise NotFoundException(resource_name="Mahasiswa", identifier=mahasiswa_id)

        from src.application.enums import MahasiswaStatus
        mahasiswa_model.status = MahasiswaStatus.DROP_OUT
        self.session.add(mahasiswa_model)
        self.session.commit()
        return True


from typing import Optional, override

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.dtos.jadwal_dto import (
    CreateJadwalDto,
    JadwalDto,
    UpdateJadwalDto,
)
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.jadwal_repository import (
    JadwalRepositoryInterface,
)
from src.ports.jadwal import GetJadwalPort
from src.repositories.database.models.jadwal import JadwalModel


class JadwalRepository(JadwalRepositoryInterface):
    def __init__(self, session_db: Session):
        self.session: Session = session_db

    @override
    def create(self, jadwal_dto: CreateJadwalDto) -> JadwalDto:
        jadwal_model = JadwalModel(
            hari=jadwal_dto.hari,
            jam_mulai=jadwal_dto.jam_mulai,
            jam_selesai=jadwal_dto.jam_selesai,
            ruangan=jadwal_dto.ruangan,
            mata_kuliah_id=jadwal_dto.mata_kuliah_id,
            dosen_id=jadwal_dto.dosen_id,
            is_active=jadwal_dto.is_active,
        )
        self.session.add(jadwal_model)
        self.session.commit()
        self.session.refresh(jadwal_model)
        return jadwal_model.to_entity()

    @override
    def read(self, get_jadwal_port: GetJadwalPort) -> list[JadwalDto]:
        stmt = select(JadwalModel)

        filters = []
        if get_jadwal_port.id:
            filters.append(JadwalModel.id == get_jadwal_port.id)
        if get_jadwal_port.hari:
            filters.append(JadwalModel.hari.ilike(f"%{get_jadwal_port.hari}%"))
        if get_jadwal_port.jam_mulai:
            filters.append(JadwalModel.jam_mulai == get_jadwal_port.jam_mulai)
        if get_jadwal_port.jam_selesai:
            filters.append(JadwalModel.jam_selesai == get_jadwal_port.jam_selesai)
        if get_jadwal_port.ruangan:
            filters.append(JadwalModel.ruangan.ilike(f"%{get_jadwal_port.ruangan}%"))
        if get_jadwal_port.mata_kuliah_id:
            filters.append(JadwalModel.mata_kuliah_id == get_jadwal_port.mata_kuliah_id)
        if get_jadwal_port.dosen_id:
            filters.append(JadwalModel.dosen_id == get_jadwal_port.dosen_id)

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_jadwal_port.order_by:
            order_column = getattr(JadwalModel, get_jadwal_port.order_by, None)
            if order_column:
                if get_jadwal_port.order and get_jadwal_port.order.lower() == "desc":
                    stmt = stmt.order_by(order_column.desc())
                else:
                    stmt = stmt.order_by(order_column.asc())

        if get_jadwal_port.limit:
            stmt = stmt.limit(get_jadwal_port.limit)
        if get_jadwal_port.page and get_jadwal_port.limit:
            stmt = stmt.offset((get_jadwal_port.page - 1) * get_jadwal_port.limit)

        jadwal_models = self.session.execute(stmt).scalars().all()
        return [j.to_entity() for j in jadwal_models]

    @override
    def update(self, jadwal_dto: UpdateJadwalDto) -> JadwalDto:
        jadwal_model: Optional[JadwalModel] = self.session.get(
            JadwalModel, jadwal_dto.id
        )
        if not jadwal_model:
            raise NotFoundException(resource_name="Jadwal", identifier=jadwal_dto.id)

        jadwal_model.hari = jadwal_dto.hari
        jadwal_model.jam_mulai = jadwal_dto.jam_mulai
        jadwal_model.jam_selesai = jadwal_dto.jam_selesai
        jadwal_model.ruangan = jadwal_dto.ruangan
        jadwal_model.mata_kuliah_id = jadwal_dto.mata_kuliah_id
        jadwal_model.dosen_id = jadwal_dto.dosen_id
        jadwal_model.is_active = jadwal_dto.is_active

        self.session.add(jadwal_model)
        self.session.commit()
        self.session.refresh(jadwal_model)
        return jadwal_model.to_entity()

    @override
    def delete(self, jadwal_id: int) -> bool:
        jadwal_model: Optional[JadwalModel] = self.session.get(JadwalModel, jadwal_id)
        if not jadwal_model:
            raise NotFoundException(resource_name="Jadwal", identifier=jadwal_id)

        jadwal_model.is_active = False
        self.session.add(jadwal_model)
        self.session.commit()
        return True

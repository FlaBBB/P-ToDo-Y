from typing import Optional, override

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.dtos.mata_kuliah_dto import (
    CreateMataKuliahDto,
    MataKuliahDto,
    UpdateMataKuliahDto,
)
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.mata_kuliah_repository import (
    MataKuliahRepositoryInterface,
)
from src.ports.mata_kuliah import GetMataKuliahPort
from src.repositories.database.models.mata_kuliah import MataKuliahModel


class MataKuliahRepository(MataKuliahRepositoryInterface):
    def __init__(self, session_db: Session):
        self.session: Session = session_db

    @override
    def create(self, mata_kuliah_dto: CreateMataKuliahDto) -> MataKuliahDto:
        mata_kuliah_model = MataKuliahModel(
            kode_mk=mata_kuliah_dto.kode_mk,
            nama_mk=mata_kuliah_dto.nama_mk,
            sks=mata_kuliah_dto.sks,
        )
        self.session.add(mata_kuliah_model)
        self.session.commit()
        self.session.refresh(mata_kuliah_model)
        return mata_kuliah_model.to_entity()

    @override
    def read(self, get_mata_kuliah_port: GetMataKuliahPort) -> list[MataKuliahDto]:
        stmt = select(MataKuliahModel)

        filters = []
        if get_mata_kuliah_port.id:
            filters.append(MataKuliahModel.id == get_mata_kuliah_port.id)
        if get_mata_kuliah_port.kode_mk:
            filters.append(MataKuliahModel.kode_mk == get_mata_kuliah_port.kode_mk)
        if get_mata_kuliah_port.nama_mk:
            filters.append(MataKuliahModel.nama_mk.ilike(f"%{get_mata_kuliah_port.nama_mk}%"))
        if get_mata_kuliah_port.sks:
            filters.append(MataKuliahModel.sks == get_mata_kuliah_port.sks)

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_mata_kuliah_port.order_by:
            order_column = getattr(MataKuliahModel, get_mata_kuliah_port.order_by, None)
            if order_column:
                if (
                    get_mata_kuliah_port.order
                    and get_mata_kuliah_port.order.lower() == "desc"
                ):
                    stmt = stmt.order_by(order_column.desc())
                else:
                    stmt = stmt.order_by(order_column.asc())

        if get_mata_kuliah_port.limit:
            stmt = stmt.limit(get_mata_kuliah_port.limit)
        if get_mata_kuliah_port.page and get_mata_kuliah_port.limit:
            stmt = stmt.offset((get_mata_kuliah_port.page - 1) * get_mata_kuliah_port.limit)

        mata_kuliah_models = self.session.execute(stmt).scalars().all()
        return [m.to_entity() for m in mata_kuliah_models]

    @override
    def update(self, mata_kuliah_dto: UpdateMataKuliahDto) -> MataKuliahDto:
        mata_kuliah_model: Optional[MataKuliahModel] = self.session.get(
            MataKuliahModel, mata_kuliah_dto.id
        )
        if not mata_kuliah_model:
            raise NotFoundException(
                resource_name="Mata Kuliah", identifier=mata_kuliah_dto.id
            )

        mata_kuliah_model.kode_mk = mata_kuliah_dto.kode_mk
        mata_kuliah_model.nama_mk = mata_kuliah_dto.nama_mk
        mata_kuliah_model.sks = mata_kuliah_dto.sks

        self.session.add(mata_kuliah_model)
        self.session.commit()
        self.session.refresh(mata_kuliah_model)
        return mata_kuliah_model.to_entity()

    @override
    def delete(self, mata_kuliah_id: int) -> bool:
        mata_kuliah_model: Optional[MataKuliahModel] = self.session.get(
            MataKuliahModel, mata_kuliah_id
        )
        if not mata_kuliah_model:
            raise NotFoundException(resource_name="Mata Kuliah", identifier=mata_kuliah_id)

        self.session.delete(mata_kuliah_model)
        self.session.commit()
        return True

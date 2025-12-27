from typing import Optional
from typing_extensions import override

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.dtos.dosen_dto import (
    CreateDosenDto,
    DosenDto,
    UpdateDosenDto,
)
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.dosen_repository import (
    DosenRepositoryInterface,
)
from src.ports.dosen import GetDosenPort
from src.repositories.database.models.dosen import DosenModel


class DosenRepository(DosenRepositoryInterface):
    def __init__(self, session_db: Session):
        self.session: Session = session_db

    @override
    def create(self, dosen_dto: CreateDosenDto) -> DosenDto:
        dosen_model = DosenModel(
            nidn=dosen_dto.nidn,
            nama=dosen_dto.nama,
            email=dosen_dto.email,
            status=dosen_dto.status,
        )
        self.session.add(dosen_model)
        self.session.commit()
        self.session.refresh(dosen_model)
        return dosen_model.to_entity()

    @override
    def read(self, get_dosen_port: GetDosenPort) -> list[DosenDto]:
        stmt = select(DosenModel)

        filters = []
        if get_dosen_port.id:
            filters.append(DosenModel.id == get_dosen_port.id)
        if get_dosen_port.nidn:
            filters.append(DosenModel.nidn == get_dosen_port.nidn)
        if get_dosen_port.nama:
            filters.append(DosenModel.nama.ilike(f"%{get_dosen_port.nama}%"))
        if get_dosen_port.email:
            filters.append(DosenModel.email.ilike(f"%{get_dosen_port.email}%"))

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_dosen_port.order_by:
            order_column = getattr(DosenModel, get_dosen_port.order_by, None)
            if order_column:
                if get_dosen_port.order and get_dosen_port.order.lower() == "desc":
                    stmt = stmt.order_by(order_column.desc())
                else:
                    stmt = stmt.order_by(order_column.asc())

        if get_dosen_port.limit:
            stmt = stmt.limit(get_dosen_port.limit)
        if get_dosen_port.page and get_dosen_port.limit:
            stmt = stmt.offset((get_dosen_port.page - 1) * get_dosen_port.limit)

        dosen_models = self.session.execute(stmt).scalars().all()
        return [d.to_entity() for d in dosen_models]

    @override
    def update(self, dosen_dto: UpdateDosenDto) -> DosenDto:
        dosen_model: Optional[DosenModel] = self.session.get(DosenModel, dosen_dto.id)
        if not dosen_model:
            raise NotFoundException(resource_name="Dosen", identifier=dosen_dto.id)

        dosen_model.nidn = dosen_dto.nidn
        dosen_model.nama = dosen_dto.nama
        dosen_model.email = dosen_dto.email
        dosen_model.status = dosen_dto.status

        self.session.add(dosen_model)
        self.session.commit()
        self.session.refresh(dosen_model)
        return dosen_model.to_entity()

    @override
    def delete(self, dosen_id: int) -> bool:
        dosen_model: Optional[DosenModel] = self.session.get(DosenModel, dosen_id)
        if not dosen_model:
            raise NotFoundException(resource_name="Dosen", identifier=dosen_id)

        from src.application.enums import DosenStatus
        dosen_model.status = DosenStatus.INACTIVE
        self.session.add(dosen_model)
        self.session.commit()
        return True

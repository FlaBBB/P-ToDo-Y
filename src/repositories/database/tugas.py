from typing import Optional, override

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.application.dtos.tugas_dto import (
    CreateTugasDto,
    TugasDto,
    UpdateTugasDto,
)
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.tugas_repository import (
    TugasRepositoryInterface,
)
from src.ports.tugas import GetTugasPort
from src.repositories.database.models.tugas import TugasModel


class TugasRepository(TugasRepositoryInterface):
    def __init__(self, session_db: Session):
        self.session: Session = session_db

    @override
    def create(self, tugas_dto: CreateTugasDto) -> TugasDto:
        tugas_model = TugasModel(
            judul=tugas_dto.judul,
            deskripsi=tugas_dto.deskripsi,
            deadline=tugas_dto.deadline,
            status=tugas_dto.status,
            mata_kuliah_id=tugas_dto.mata_kuliah_id,
            mahasiswa_id=tugas_dto.mahasiswa_id,
        )
        self.session.add(tugas_model)
        self.session.commit()
        self.session.refresh(tugas_model)
        return tugas_model.to_entity()

    @override
    def read(self, get_tugas_port: GetTugasPort) -> list[TugasDto]:
        stmt = select(TugasModel)

        filters = []
        if get_tugas_port.id:
            filters.append(TugasModel.id == get_tugas_port.id)
        if get_tugas_port.judul:
            filters.append(TugasModel.judul.ilike(f"%{get_tugas_port.judul}%"))
        if get_tugas_port.status:
            filters.append(TugasModel.status == get_tugas_port.status)
        if get_tugas_port.mata_kuliah_id:
            filters.append(TugasModel.mata_kuliah_id == get_tugas_port.mata_kuliah_id)
        if get_tugas_port.mahasiswa_id:
            filters.append(TugasModel.mahasiswa_id == get_tugas_port.mahasiswa_id)
        if get_tugas_port.deadline_from:
            filters.append(TugasModel.deadline >= get_tugas_port.deadline_from)
        if get_tugas_port.deadline_to:
            filters.append(TugasModel.deadline <= get_tugas_port.deadline_to)

        if filters:
            stmt = stmt.where(and_(*filters))

        if get_tugas_port.order_by:
            order_column = getattr(TugasModel, get_tugas_port.order_by, None)
            if order_column:
                if (
                    get_tugas_port.order
                    and get_tugas_port.order.lower() == "desc"
                ):
                    stmt = stmt.order_by(order_column.desc())
                else:
                    stmt = stmt.order_by(order_column.asc())

        if get_tugas_port.limit:
            stmt = stmt.limit(get_tugas_port.limit)
        if get_tugas_port.page and get_tugas_port.limit:
            stmt = stmt.offset((get_tugas_port.page - 1) * get_tugas_port.limit)

        tugas_models = self.session.execute(stmt).scalars().all()
        return [t.to_entity() for t in tugas_models]

    @override
    def update(self, tugas_dto: UpdateTugasDto) -> TugasDto:
        tugas_model: Optional[TugasModel] = self.session.get(
            TugasModel, tugas_dto.id
        )
        if not tugas_model:
            raise NotFoundException(
                resource_name="Tugas", identifier=tugas_dto.id
            )

        tugas_model.judul = tugas_dto.judul
        tugas_model.deskripsi = tugas_dto.deskripsi
        tugas_model.deadline = tugas_dto.deadline
        tugas_model.status = tugas_dto.status
        tugas_model.mata_kuliah_id = tugas_dto.mata_kuliah_id
        tugas_model.mahasiswa_id = tugas_dto.mahasiswa_id

        self.session.add(tugas_model)
        self.session.commit()
        self.session.refresh(tugas_model)
        return tugas_model.to_entity()

    @override
    def delete(self, tugas_id: int) -> bool:
        tugas_model: Optional[TugasModel] = self.session.get(
            TugasModel, tugas_id
        )
        if not tugas_model:
            raise NotFoundException(resource_name="Tugas", identifier=tugas_id)

        from src.application.dtos.tugas_dto import StatusTugas
        tugas_model.status = StatusTugas.CANCELLED
        self.session.add(tugas_model)
        self.session.commit()
        return True

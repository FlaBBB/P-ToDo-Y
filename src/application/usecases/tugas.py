from src.application.dtos.tugas_dto import (
    CreateTugasDto,
    TugasDto,
    UpdateTugasDto,
)
from src.application.exceptions import (
    InvalidInputException,
    NotFoundException,
)
from src.application.usecases.interfaces.tugas_repository import (
    TugasRepositoryInterface,
)
from src.ports.tugas import GetTugasPort


class TugasService:
    def __init__(self, tugas_repo: TugasRepositoryInterface):
        self.tugas_repo = tugas_repo

    def create(self, tugas_dto: CreateTugasDto) -> TugasDto:
        if not tugas_dto.judul:
            raise InvalidInputException("Judul cannot be empty")

        # Basic validation, more complex logic can be added here

        return self.tugas_repo.create(tugas_dto)

    def read(self, get_tugas_port: GetTugasPort) -> list[TugasDto]:
        return self.tugas_repo.read(get_tugas_port)

    def update(self, tugas_dto: UpdateTugasDto) -> TugasDto:
        existing_tugas = self.tugas_repo.read(GetTugasPort(id=tugas_dto.id))
        if not existing_tugas:
            raise NotFoundException(resource_name="Tugas", identifier=tugas_dto.id)

        return self.tugas_repo.update(tugas_dto)

    def delete(self, tugas_id: int) -> bool:
        existing_tugas = self.tugas_repo.read(GetTugasPort(id=tugas_id))
        if not existing_tugas:
            raise NotFoundException(resource_name="Tugas", identifier=tugas_id)
        return self.tugas_repo.delete(tugas_id)

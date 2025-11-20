from src.application.dtos.mata_kuliah_dto import (
    CreateMataKuliahDto,
    MataKuliahDto,
    UpdateMataKuliahDto,
)
from src.application.exceptions import (
    DuplicateEntryException,
    InvalidInputException,
    NotFoundException,
)
from src.application.usecases.interfaces.mata_kuliah_repository import (
    MataKuliahRepositoryInterface,
)
from src.ports.mata_kuliah import GetMataKuliahPort


class MataKuliahService:
    def __init__(self, mata_kuliah_repo: MataKuliahRepositoryInterface):
        self.mata_kuliah_repo = mata_kuliah_repo

    def create(self, mata_kuliah_dto: CreateMataKuliahDto) -> MataKuliahDto:
        if not mata_kuliah_dto.kode_mk:
            raise InvalidInputException("Kode MK cannot be empty")
        if not mata_kuliah_dto.nama_mk:
            raise InvalidInputException("Nama MK cannot be empty")
        if mata_kuliah_dto.sks <= 0:
            raise InvalidInputException("SKS must be greater than 0")

        existing_mk = self.mata_kuliah_repo.read(
            GetMataKuliahPort(kode_mk=mata_kuliah_dto.kode_mk)
        )
        if existing_mk:
            raise DuplicateEntryException(
                resource_name="Mata Kuliah", identifier=mata_kuliah_dto.kode_mk
            )

        return self.mata_kuliah_repo.create(mata_kuliah_dto)

    def read(self, get_mata_kuliah_port: GetMataKuliahPort) -> list[MataKuliahDto]:
        return self.mata_kuliah_repo.read(get_mata_kuliah_port)

    def update(self, mata_kuliah_dto: UpdateMataKuliahDto) -> MataKuliahDto:
        existing_mk = self.mata_kuliah_repo.read(
            GetMataKuliahPort(id=mata_kuliah_dto.id)
        )
        if not existing_mk:
            raise NotFoundException(
                resource_name="Mata Kuliah", identifier=mata_kuliah_dto.id
            )

        # Check if kode_mk is being changed to one that already exists
        if mata_kuliah_dto.kode_mk != existing_mk[0].kode_mk:
            duplicate_check = self.mata_kuliah_repo.read(
                GetMataKuliahPort(kode_mk=mata_kuliah_dto.kode_mk)
            )
            if duplicate_check:
                raise DuplicateEntryException(
                    resource_name="Mata Kuliah", identifier=mata_kuliah_dto.kode_mk
                )

        return self.mata_kuliah_repo.update(mata_kuliah_dto)

    def delete(self, mata_kuliah_id: int) -> bool:
        existing_mk = self.mata_kuliah_repo.read(GetMataKuliahPort(id=mata_kuliah_id))
        if not existing_mk:
            raise NotFoundException(
                resource_name="Mata Kuliah", identifier=mata_kuliah_id
            )
        return self.mata_kuliah_repo.delete(mata_kuliah_id)

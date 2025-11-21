from src.application.dtos.jadwal_dto import (
    CreateJadwalDto,
    JadwalDto,
    UpdateJadwalDto,
)
from src.application.exceptions import (
    InvalidInputException,
    NotFoundException,
)
from src.application.usecases.interfaces.jadwal_repository import (
    JadwalRepositoryInterface,
)
from src.ports.jadwal import GetJadwalPort


class JadwalService:
    def __init__(self, jadwal_repo: JadwalRepositoryInterface):
        self.jadwal_repo = jadwal_repo

    def create(self, jadwal_dto: CreateJadwalDto) -> JadwalDto:
        if not jadwal_dto.hari:
            raise InvalidInputException("Hari cannot be empty")
        if not jadwal_dto.ruangan:
            raise InvalidInputException("Ruangan cannot be empty")
        if jadwal_dto.jam_mulai >= jadwal_dto.jam_selesai:
            raise InvalidInputException("Jam mulai must be before jam selesai")

        # TODO: Validate mata_kuliah_id and dosen_id existence
        # (can be done via repo or separate service call)
        # For now, we rely on foreign key constraints in the database
        # to fail if they don't exist.

        return self.jadwal_repo.create(jadwal_dto)

    def read(self, get_jadwal_port: GetJadwalPort) -> list[JadwalDto]:
        return self.jadwal_repo.read(get_jadwal_port)

    def update(self, jadwal_dto: UpdateJadwalDto) -> JadwalDto:
        existing_jadwal = self.jadwal_repo.read(GetJadwalPort(id=jadwal_dto.id))
        if not existing_jadwal:
            raise NotFoundException(resource_name="Jadwal", identifier=jadwal_dto.id)

        if jadwal_dto.jam_mulai >= jadwal_dto.jam_selesai:
            raise InvalidInputException("Jam mulai must be before jam selesai")

        return self.jadwal_repo.update(jadwal_dto)

    def delete(self, jadwal_id: int) -> bool:
        existing_jadwal = self.jadwal_repo.read(GetJadwalPort(id=jadwal_id))
        if not existing_jadwal:
            raise NotFoundException(resource_name="Jadwal", identifier=jadwal_id)
        return self.jadwal_repo.delete(jadwal_id)

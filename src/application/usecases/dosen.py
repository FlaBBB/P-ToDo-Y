from src.application.dtos.dosen_dto import (
    CreateDosenDto,
    DosenDto,
    UpdateDosenDto,
)
from src.application.exceptions import (
    DuplicateEntryException,
    InvalidInputException,
    NotFoundException,
)
from src.application.usecases.interfaces.dosen_repository import (
    DosenRepositoryInterface,
)
from src.ports.dosen import GetDosenPort


class DosenService:
    def __init__(self, dosen_repo: DosenRepositoryInterface):
        self.dosen_repo = dosen_repo

    def create(self, dosen_dto: CreateDosenDto) -> DosenDto:
        if not dosen_dto.nidn:
            raise InvalidInputException("NIDN cannot be empty")
        if not dosen_dto.nama:
            raise InvalidInputException("Nama cannot be empty")
        if not dosen_dto.email:
            raise InvalidInputException("Email cannot be empty")

        existing_dosen = self.dosen_repo.read(
            GetDosenPort(nidn=dosen_dto.nidn)
        )
        if existing_dosen:
            raise DuplicateEntryException(
                resource_name="Dosen", identifier=dosen_dto.nidn
            )
        
        existing_email = self.dosen_repo.read(
            GetDosenPort(email=dosen_dto.email)
        )
        if existing_email:
            raise DuplicateEntryException(
                resource_name="Dosen", identifier=dosen_dto.email
            )

        return self.dosen_repo.create(dosen_dto)

    def read(self, get_dosen_port: GetDosenPort) -> list[DosenDto]:
        return self.dosen_repo.read(get_dosen_port)

    def update(self, dosen_dto: UpdateDosenDto) -> DosenDto:
        existing_dosen = self.dosen_repo.read(
            GetDosenPort(id=dosen_dto.id)
        )
        if not existing_dosen:
            raise NotFoundException(
                resource_name="Dosen", identifier=dosen_dto.id
            )

        # Check if nidn is being changed to one that already exists
        if dosen_dto.nidn != existing_dosen[0].nidn:
            duplicate_check = self.dosen_repo.read(
                GetDosenPort(nidn=dosen_dto.nidn)
            )
            if duplicate_check:
                raise DuplicateEntryException(
                    resource_name="Dosen", identifier=dosen_dto.nidn
                )
        
        # Check if email is being changed to one that already exists
        if dosen_dto.email != existing_dosen[0].email:
            duplicate_check_email = self.dosen_repo.read(
                GetDosenPort(email=dosen_dto.email)
            )
            if duplicate_check_email:
                raise DuplicateEntryException(
                    resource_name="Dosen", identifier=dosen_dto.email
                )

        return self.dosen_repo.update(dosen_dto)

    def delete(self, dosen_id: int) -> bool:
        existing_dosen = self.dosen_repo.read(GetDosenPort(id=dosen_id))
        if not existing_dosen:
            raise NotFoundException(
                resource_name="Dosen", identifier=dosen_id
            )
        return self.dosen_repo.delete(dosen_id)

from src.application.dtos.mahasiswa_dto import (
    CreateMahasiswaDto,
    MahasiswaDto,
    UpdateMahasiswaDto,
)
from src.application.exceptions import DuplicateEntryException
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.ports.mahasiswa import GetMahasiswaPort


class MahasiswaService:
    def __init__(self, mahasiswa_repo: MahasiswaRepositoryInterface) -> None:
        self.mahasiswa_repo: MahasiswaRepositoryInterface = mahasiswa_repo

    def create(self, mahasiswa: CreateMahasiswaDto) -> MahasiswaDto:
        existing_mahasiswa = self.mahasiswa_repo.read(
            GetMahasiswaPort(nim=mahasiswa.nim)
        )
        if existing_mahasiswa:
            raise DuplicateEntryException(
                resource_name="Mahasiswa", field_name="NIM", field_value=mahasiswa.nim
            )
        return self.mahasiswa_repo.create(mahasiswa)

    def read(self, get_mahasiswa_port: GetMahasiswaPort) -> list[MahasiswaDto]:
        return self.mahasiswa_repo.read(get_mahasiswa_port)

    def update(self, mahasiswa: UpdateMahasiswaDto) -> MahasiswaDto:
        return self.mahasiswa_repo.update(mahasiswa)

    def delete(self, mahasiswa_id: int) -> bool:
        return self.mahasiswa_repo.delete(mahasiswa_id)

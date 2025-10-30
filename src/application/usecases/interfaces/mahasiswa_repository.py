from abc import ABC, abstractmethod

from src.application.dtos.mahasiswa_dto import (
    CreateMahasiswaDto,
    MahasiswaDto,
    UpdateMahasiswaDto,
)
from src.ports.mahasiswa import GetMahasiswaPort


class MahasiswaRepositoryInterface(ABC):
    @abstractmethod
    def create(self, mahasiswa_dto: CreateMahasiswaDto) -> MahasiswaDto:
        raise NotImplementedError("Subclasses must implement create method")

    @abstractmethod
    def read(self, get_mahasiswa_port: GetMahasiswaPort) -> list[MahasiswaDto]:
        raise NotImplementedError("Subclasses must implement read method")

    @abstractmethod
    def update(self, mahasiswa_dto: UpdateMahasiswaDto) -> MahasiswaDto:
        raise NotImplementedError("Subclasses must implement update method")

    @abstractmethod
    def delete(self, mahasiswa_id: int) -> bool:
        raise NotImplementedError("Subclasses must implement delete method")

from abc import ABC, abstractmethod

from src.application.dtos.dosen_dto import (
    CreateDosenDto,
    DosenDto,
    UpdateDosenDto,
)
from src.ports.dosen import GetDosenPort


class DosenRepositoryInterface(ABC):
    @abstractmethod
    def create(self, dosen_dto: CreateDosenDto) -> DosenDto:
        pass

    @abstractmethod
    def read(self, get_dosen_port: GetDosenPort) -> list[DosenDto]:
        pass

    @abstractmethod
    def update(self, dosen_dto: UpdateDosenDto) -> DosenDto:
        pass

    @abstractmethod
    def delete(self, dosen_id: int) -> bool:
        pass

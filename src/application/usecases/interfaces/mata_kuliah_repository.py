from abc import ABC, abstractmethod

from src.application.dtos.mata_kuliah_dto import (
    CreateMataKuliahDto,
    MataKuliahDto,
    UpdateMataKuliahDto,
)
from src.ports.mata_kuliah import GetMataKuliahPort


class MataKuliahRepositoryInterface(ABC):
    @abstractmethod
    def create(self, mata_kuliah_dto: CreateMataKuliahDto) -> MataKuliahDto:
        pass

    @abstractmethod
    def read(self, get_mata_kuliah_port: GetMataKuliahPort) -> list[MataKuliahDto]:
        pass

    @abstractmethod
    def update(self, mata_kuliah_dto: UpdateMataKuliahDto) -> MataKuliahDto:
        pass

    @abstractmethod
    def delete(self, mata_kuliah_id: int) -> bool:
        pass

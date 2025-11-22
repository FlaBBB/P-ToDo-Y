from abc import ABC, abstractmethod

from src.application.dtos.tugas_dto import (
    CreateTugasDto,
    TugasDto,
    UpdateTugasDto,
)
from src.ports.tugas import GetTugasPort


class TugasRepositoryInterface(ABC):
    @abstractmethod
    def create(self, tugas_dto: CreateTugasDto) -> TugasDto:
        pass

    @abstractmethod
    def read(self, get_tugas_port: GetTugasPort) -> list[TugasDto]:
        pass

    @abstractmethod
    def update(self, tugas_dto: UpdateTugasDto) -> TugasDto:
        pass

    @abstractmethod
    def delete(self, tugas_id: int) -> bool:
        pass

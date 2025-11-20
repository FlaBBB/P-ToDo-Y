from abc import ABC, abstractmethod

from src.application.dtos.jadwal_dto import (
    CreateJadwalDto,
    JadwalDto,
    UpdateJadwalDto,
)
from src.ports.jadwal import GetJadwalPort


class JadwalRepositoryInterface(ABC):
    @abstractmethod
    def create(self, jadwal_dto: CreateJadwalDto) -> JadwalDto:
        pass

    @abstractmethod
    def read(self, get_jadwal_port: GetJadwalPort) -> list[JadwalDto]:
        pass

    @abstractmethod
    def update(self, jadwal_dto: UpdateJadwalDto) -> JadwalDto:
        pass

    @abstractmethod
    def delete(self, jadwal_id: int) -> bool:
        pass

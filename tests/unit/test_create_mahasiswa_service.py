from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.dtos.mahasiswa_dto import MahasiswaDto
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.application.usecases.mahasiswa import MahasiswaService
from src.ports.mahasiswa import GetMahasiswaPort


@pytest.fixture
def mahasiswa_service(mock_mahasiswa_repo: MagicMock) -> MahasiswaService:
    """Fixture for MahasiswaService with a mocked repository."""
    return MahasiswaService(mahasiswa_repo=mock_mahasiswa_repo)
from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.dtos.mahasiswa_dto import MahasiswaDto, UpdateMahasiswaDto
from src.application.enums import MahasiswaStatus
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.application.usecases.mahasiswa import MahasiswaService


@pytest.fixture
def mock_mahasiswa_repo() -> MagicMock:
    """Fixture for a mocked MahasiswaRepositoryInterface."""
    return MagicMock(spec=MahasiswaRepositoryInterface)


@pytest.fixture
def mahasiswa_service(mock_mahasiswa_repo: MagicMock) -> MahasiswaService:
    """Fixture for MahasiswaService with a mocked repository."""
    return MahasiswaService(mahasiswa_repo=mock_mahasiswa_repo)


def test_update_mahasiswa_success(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test updating a Mahasiswa successfully.
    """
    update_dto = UpdateMahasiswaDto(
        id=1,
        nim="2024000001",
        nama="John Updated",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
        status=MahasiswaStatus.ACTIVE,
    )

    expected_result = MahasiswaDto(
        id=1,
        nim="2024000001",
        nama="John Updated",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
        status=MahasiswaStatus.ACTIVE,
    )

    mock_mahasiswa_repo.update.return_value = expected_result

    result = mahasiswa_service.update(update_dto)

    mock_mahasiswa_repo.update.assert_called_once_with(update_dto)
    assert result == expected_result


def test_update_mahasiswa_not_found(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test updating a non-existent Mahasiswa raises NotFoundException.
    """
    update_dto = UpdateMahasiswaDto(
        id=999,
        nim="2024000999",
        nama="Non Existent",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
        status=MahasiswaStatus.ACTIVE,
    )

    mock_mahasiswa_repo.update.side_effect = NotFoundException(
        resource_name="Mahasiswa", identifier=999
    )

    with pytest.raises(NotFoundException) as exc_info:
        mahasiswa_service.update(update_dto)

    assert "Mahasiswa with ID/NIM '999' not found" in str(exc_info.value.message)
    mock_mahasiswa_repo.update.assert_called_once_with(update_dto)

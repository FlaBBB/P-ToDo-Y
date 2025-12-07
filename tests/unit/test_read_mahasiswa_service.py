from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.dtos.mahasiswa_dto import MahasiswaDto
from src.application.enums import MahasiswaStatus
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.application.usecases.mahasiswa import MahasiswaService
from src.ports.mahasiswa import GetMahasiswaPort


@pytest.fixture
def mock_mahasiswa_repo() -> MagicMock:
    """Fixture for a mocked MahasiswaRepositoryInterface."""
    return MagicMock(spec=MahasiswaRepositoryInterface)


@pytest.fixture
def mahasiswa_service(mock_mahasiswa_repo: MagicMock) -> MahasiswaService:
    """Fixture for MahasiswaService with a mocked repository."""
    return MahasiswaService(mahasiswa_repo=mock_mahasiswa_repo)


def test_read_all_mahasiswa(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test that reading all Mahasiswa returns the expected list of DTOs.
    """
    expected_mahasiswa_dtos = [
        MahasiswaDto(
            id=1,
            nim="2023000001",
            nama="Test Name 1",
            kelas="TI-3E",
            tempat_lahir="City 1",
            tanggal_lahir=date(2000, 1, 1),
            status=MahasiswaStatus.ACTIVE,
        ),
        MahasiswaDto(
            id=2,
            nim="2023000002",
            nama="Test Name 2",
            kelas="SIB-5F",
            tempat_lahir="City 2",
            tanggal_lahir=date(2001, 2, 2),
            status=MahasiswaStatus.ACTIVE,
        ),
    ]
    mock_mahasiswa_repo.read.return_value = expected_mahasiswa_dtos

    result = mahasiswa_service.read(GetMahasiswaPort())

    mock_mahasiswa_repo.read.assert_called_once_with(GetMahasiswaPort())
    assert result == expected_mahasiswa_dtos


def test_read_mahasiswa_by_nim(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test that reading Mahasiswa by NIM returns the specific DTO.
    """
    nim_to_find = "2023000001"
    expected_mahasiswa_dto = [
        MahasiswaDto(
            id=1,
            nim=nim_to_find,
            nama="Test Name 1",
            kelas="TI-3E",
            tempat_lahir="City 1",
            tanggal_lahir=date(2000, 1, 1),
            status=MahasiswaStatus.ACTIVE,
        ),
    ]
    mock_mahasiswa_repo.read.return_value = expected_mahasiswa_dto

    port = GetMahasiswaPort(nim=nim_to_find)
    result = mahasiswa_service.read(port)

    mock_mahasiswa_repo.read.assert_called_once_with(port)
    assert result == expected_mahasiswa_dto


def test_read_mahasiswa_not_found(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test that reading Mahasiswa with non-existent criteria returns an empty list.
    """
    mock_mahasiswa_repo.read.return_value = []

    port = GetMahasiswaPort(nim="nonexistent")
    result = mahasiswa_service.read(port)

    mock_mahasiswa_repo.read.assert_called_once_with(port)
    assert result == []


def test_read_mahasiswa_with_pagination(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test reading Mahasiswa with pagination parameters.
    """
    expected_mahasiswa_dtos = [
        MahasiswaDto(
            id=1,
            nim="2023000001",
            nama="Test Name 1",
            kelas="TI-3E",
            tempat_lahir="City 1",
            tanggal_lahir=date(2000, 1, 1),
            status=MahasiswaStatus.ACTIVE,
        ),
    ]
    mock_mahasiswa_repo.read.return_value = expected_mahasiswa_dtos

    port = GetMahasiswaPort(limit=1, page=1)
    result = mahasiswa_service.read(port)

    mock_mahasiswa_repo.read.assert_called_once_with(port)
    assert result == expected_mahasiswa_dtos


def test_read_mahasiswa_with_ordering(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test reading Mahasiswa with ordering parameters.
    """
    expected_mahasiswa_dtos = [
        MahasiswaDto(
            id=2,
            nim="2023000002",
            nama="Test Name 2",
            kelas="SIB-5F",
            tempat_lahir="City 2",
            tanggal_lahir=date(2001, 2, 2),
            status=MahasiswaStatus.ACTIVE,
        ),
        MahasiswaDto(
            id=1,
            nim="2023000001",
            nama="Test Name 1",
            kelas="TI-3E",
            tempat_lahir="City 1",
            tanggal_lahir=date(2000, 1, 1),
            status=MahasiswaStatus.ACTIVE,
        ),
    ]
    mock_mahasiswa_repo.read.return_value = expected_mahasiswa_dtos

    port = GetMahasiswaPort(order_by="nama", order="desc")
    result = mahasiswa_service.read(port)

    mock_mahasiswa_repo.read.assert_called_once_with(port)
    assert result == expected_mahasiswa_dtos

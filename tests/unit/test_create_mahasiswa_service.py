from datetime import date
from unittest.mock import MagicMock

import pytest

from src.application.dtos.mahasiswa_dto import CreateMahasiswaDto, MahasiswaDto
from src.application.enums import MahasiswaStatus
from src.application.exceptions import DuplicateEntryException
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


def test_create_mahasiswa_success(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test creating a new Mahasiswa successfully.
    """
    create_dto = CreateMahasiswaDto(
        nim="2024000001",
        nama="John Doe",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
    )

    expected_result = MahasiswaDto(
        id=1,
        nim="2024000001",
        nama="John Doe",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
        status=MahasiswaStatus.ACTIVE,
    )

    # Mock: NIM doesn't exist yet
    mock_mahasiswa_repo.read.return_value = []
    # Mock: Create returns the new mahasiswa
    mock_mahasiswa_repo.create.return_value = expected_result

    result = mahasiswa_service.create(create_dto)

    # Verify repository was called to check for existing NIM
    mock_mahasiswa_repo.read.assert_called_once_with(
        GetMahasiswaPort(nim=create_dto.nim)
    )
    # Verify repository was called to create
    mock_mahasiswa_repo.create.assert_called_once_with(create_dto)
    # Verify result
    assert result == expected_result


def test_create_mahasiswa_duplicate_nim(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test creating a Mahasiswa with a duplicate NIM raises DuplicateEntryException.
    """
    create_dto = CreateMahasiswaDto(
        nim="2024000001",
        nama="John Doe",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
    )

    existing_mahasiswa = [
        MahasiswaDto(
            id=1,
            nim="2024000001",
            nama="Existing Student",
            kelas="TI-3B",
            tempat_lahir="Bandung",
            tanggal_lahir=date(2001, 1, 1),
            status=MahasiswaStatus.ACTIVE,
        )
    ]

    # Mock: NIM already exists
    mock_mahasiswa_repo.read.return_value = existing_mahasiswa

    with pytest.raises(DuplicateEntryException) as exc_info:
        mahasiswa_service.create(create_dto)

    assert "2024000001" in str(exc_info.value.message)
    mock_mahasiswa_repo.read.assert_called_once_with(
        GetMahasiswaPort(nim=create_dto.nim)
    )
    # Verify create was NOT called
    mock_mahasiswa_repo.create.assert_not_called()


def test_create_mahasiswa_empty_nim_allowed(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test creating a Mahasiswa with empty NIM is allowed (no validation).
    TODO: Add validation for empty fields in the service layer.
    """
    create_dto = CreateMahasiswaDto(
        nim="",
        nama="John Doe",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
    )

    expected_result = MahasiswaDto(
        id=1,
        nim="",
        nama="John Doe",
        kelas="TI-3A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 5, 15),
        status=MahasiswaStatus.ACTIVE,
    )

    # Mock: No existing mahasiswa
    mock_mahasiswa_repo.read.return_value = []
    mock_mahasiswa_repo.create.return_value = expected_result

    result = mahasiswa_service.create(create_dto)

    assert result == expected_result
    mock_mahasiswa_repo.create.assert_called_once_with(create_dto)


def test_create_mahasiswa_repository_called_correctly(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test that the repository methods are called with correct parameters.
    """
    create_dto = CreateMahasiswaDto(
        nim="2024000002",
        nama="Jane Doe",
        kelas="SIB-2B",
        tempat_lahir="Bandung",
        tanggal_lahir=date(2003, 8, 20),
    )

    expected_result = MahasiswaDto(
        id=2,
        nim="2024000002",
        nama="Jane Doe",
        kelas="SIB-2B",
        tempat_lahir="Bandung",
        tanggal_lahir=date(2003, 8, 20),
        status=MahasiswaStatus.ACTIVE,
    )

    mock_mahasiswa_repo.read.return_value = []
    mock_mahasiswa_repo.create.return_value = expected_result

    result = mahasiswa_service.create(create_dto)

    # Verify read was called first to check for duplicates
    assert mock_mahasiswa_repo.read.call_count == 1
    # Verify create was called with the DTO
    mock_mahasiswa_repo.create.assert_called_once_with(create_dto)
    assert result == expected_result


def test_create_mahasiswa_with_special_characters(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test creating a Mahasiswa with special characters in name.
    """
    create_dto = CreateMahasiswaDto(
        nim="2024000003",
        nama="O'Brien-Smith",
        kelas="TI-1C",
        tempat_lahir="New York",
        tanggal_lahir=date(2004, 3, 10),
    )

    expected_result = MahasiswaDto(
        id=3,
        nim="2024000003",
        nama="O'Brien-Smith",
        kelas="TI-1C",
        tempat_lahir="New York",
        tanggal_lahir=date(2004, 3, 10),
        status=MahasiswaStatus.ACTIVE,
    )

    mock_mahasiswa_repo.read.return_value = []
    mock_mahasiswa_repo.create.return_value = expected_result

    result = mahasiswa_service.create(create_dto)

    assert result == expected_result
    assert result.nama == "O'Brien-Smith"

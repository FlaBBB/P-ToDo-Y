from datetime import time
from unittest.mock import MagicMock

import pytest

from src.application.dtos.jadwal_dto import JadwalDto
from src.application.usecases.interfaces.jadwal_repository import (
    JadwalRepositoryInterface,
)
from src.application.usecases.jadwal import JadwalService
from src.ports.jadwal import GetJadwalPort


@pytest.fixture
def mock_jadwal_repo() -> MagicMock:
    """Fixture for a mocked JadwalRepositoryInterface."""
    return MagicMock(spec=JadwalRepositoryInterface)


@pytest.fixture
def jadwal_service(mock_jadwal_repo: MagicMock) -> JadwalService:
    """Fixture for JadwalService with a mocked repository."""
    return JadwalService(jadwal_repo=mock_jadwal_repo)


def test_read_all_jadwal_success(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading all jadwal successfully.
    """
    expected_jadwal_list = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        ),
        JadwalDto(
            id=2,
            hari="Selasa",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="R102",
            mata_kuliah_id=2,
            dosen_id=2,
        ),
    ]

    get_port = GetJadwalPort()
    mock_jadwal_repo.read.return_value = expected_jadwal_list

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal_list
    assert len(result) == 2
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_by_id_success(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading a specific jadwal by ID.
    """
    expected_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        )
    ]

    get_port = GetJadwalPort(id=1)
    mock_jadwal_repo.read.return_value = expected_jadwal

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal
    assert len(result) == 1
    assert result[0].id == 1
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_by_mata_kuliah_id(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading jadwal filtered by mata_kuliah_id.
    """
    expected_jadwal_list = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        ),
        JadwalDto(
            id=3,
            hari="Rabu",
            jam_mulai=time(13, 0),
            jam_selesai=time(15, 0),
            ruangan="R103",
            mata_kuliah_id=1,
            dosen_id=1,
        ),
    ]

    get_port = GetJadwalPort(mata_kuliah_id=1)
    mock_jadwal_repo.read.return_value = expected_jadwal_list

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal_list
    assert len(result) == 2
    assert all(jadwal.mata_kuliah_id == 1 for jadwal in result)
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_by_dosen_id(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading jadwal filtered by dosen_id.
    """
    expected_jadwal_list = [
        JadwalDto(
            id=2,
            hari="Selasa",
            jam_mulai=time(10, 0),
            jam_selesai=time(12, 0),
            ruangan="R102",
            mata_kuliah_id=2,
            dosen_id=2,
        )
    ]

    get_port = GetJadwalPort(dosen_id=2)
    mock_jadwal_repo.read.return_value = expected_jadwal_list

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal_list
    assert len(result) == 1
    assert result[0].dosen_id == 2
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_by_hari(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading jadwal filtered by hari.
    """
    expected_jadwal_list = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        ),
        JadwalDto(
            id=4,
            hari="Senin",
            jam_mulai=time(13, 0),
            jam_selesai=time(15, 0),
            ruangan="R104",
            mata_kuliah_id=3,
            dosen_id=3,
        ),
    ]

    get_port = GetJadwalPort(hari="Senin")
    mock_jadwal_repo.read.return_value = expected_jadwal_list

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal_list
    assert len(result) == 2
    assert all(jadwal.hari == "Senin" for jadwal in result)
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_empty_result(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading jadwal when no results are found.
    """
    get_port = GetJadwalPort(id=999)
    mock_jadwal_repo.read.return_value = []

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == []
    assert len(result) == 0
    mock_jadwal_repo.read.assert_called_once_with(get_port)


def test_read_jadwal_multiple_filters(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test reading jadwal with multiple filter criteria.
    """
    expected_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        )
    ]

    get_port = GetJadwalPort(hari="Senin", mata_kuliah_id=1, dosen_id=1)
    mock_jadwal_repo.read.return_value = expected_jadwal

    # Act
    result = jadwal_service.read(get_port)

    # Assert
    assert result == expected_jadwal
    assert len(result) == 1
    mock_jadwal_repo.read.assert_called_once_with(get_port)

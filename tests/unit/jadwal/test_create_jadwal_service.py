from datetime import time
from unittest.mock import MagicMock

import pytest

from src.application.dtos.jadwal_dto import CreateJadwalDto, JadwalDto
from src.application.exceptions import InvalidInputException
from src.application.usecases.interfaces.jadwal_repository import (
    JadwalRepositoryInterface,
)
from src.application.usecases.jadwal import JadwalService


@pytest.fixture
def mock_jadwal_repo() -> MagicMock:
    """Fixture for a mocked JadwalRepositoryInterface."""
    return MagicMock(spec=JadwalRepositoryInterface)


@pytest.fixture
def jadwal_service(mock_jadwal_repo: MagicMock) -> JadwalService:
    """Fixture for JadwalService with a mocked repository."""
    return JadwalService(jadwal_repo=mock_jadwal_repo)


def test_create_jadwal_success(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test creating a new Jadwal successfully.
    """
    create_dto = CreateJadwalDto(
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    expected_result = JadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    # Mock: repository returns created jadwal
    mock_jadwal_repo.create.return_value = expected_result

    # Act
    result = jadwal_service.create(create_dto)

    # Assert
    assert result == expected_result
    mock_jadwal_repo.create.assert_called_once_with(create_dto)


def test_create_jadwal_empty_hari_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that creating jadwal with empty hari raises InvalidInputException.
    """
    create_dto = CreateJadwalDto(
        hari="",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.create(create_dto)

    assert "Hari cannot be empty" in str(exc_info.value)
    mock_jadwal_repo.create.assert_not_called()


def test_create_jadwal_empty_ruangan_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that creating jadwal with empty ruangan raises InvalidInputException.
    """
    create_dto = CreateJadwalDto(
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.create(create_dto)

    assert "Ruangan cannot be empty" in str(exc_info.value)
    mock_jadwal_repo.create.assert_not_called()


def test_create_jadwal_invalid_time_range_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that creating jadwal with jam_mulai >= jam_selesai raises InvalidInputException.
    """
    create_dto = CreateJadwalDto(
        hari="Senin",
        jam_mulai=time(10, 0),
        jam_selesai=time(8, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.create(create_dto)

    assert "Jam mulai must be before jam selesai" in str(exc_info.value)
    mock_jadwal_repo.create.assert_not_called()


def test_create_jadwal_same_start_and_end_time_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that creating jadwal with same jam_mulai and jam_selesai raises InvalidInputException.
    """
    create_dto = CreateJadwalDto(
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(8, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.create(create_dto)

    assert "Jam mulai must be before jam selesai" in str(exc_info.value)
    mock_jadwal_repo.create.assert_not_called()


def test_create_jadwal_with_different_days(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test creating jadwal with various valid day names.
    """
    days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

    for idx, day in enumerate(days):
        create_dto = CreateJadwalDto(
            hari=day,
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        )

        expected_result = JadwalDto(
            id=idx + 1,
            hari=day,
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
        )

        mock_jadwal_repo.create.return_value = expected_result

        # Act
        result = jadwal_service.create(create_dto)

        # Assert
        assert result.hari == day
        assert result.id == idx + 1


def test_create_jadwal_with_edge_case_times(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test creating jadwal with edge case time values (e.g., midnight to early morning).
    """
    create_dto = CreateJadwalDto(
        hari="Senin",
        jam_mulai=time(0, 0),
        jam_selesai=time(23, 59),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    expected_result = JadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(0, 0),
        jam_selesai=time(23, 59),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
    )

    mock_jadwal_repo.create.return_value = expected_result

    # Act
    result = jadwal_service.create(create_dto)

    # Assert
    assert result == expected_result
    mock_jadwal_repo.create.assert_called_once_with(create_dto)

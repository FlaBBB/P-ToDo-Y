from datetime import time
from unittest.mock import MagicMock

import pytest

from src.application.dtos.jadwal_dto import JadwalDto, UpdateJadwalDto
from src.application.exceptions import InvalidInputException, NotFoundException
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


def test_update_jadwal_success(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test updating an existing jadwal successfully.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Selasa",
        jam_mulai=time(10, 0),
        jam_selesai=time(12, 0),
        ruangan="R102",
        mata_kuliah_id=2,
        dosen_id=2,
        is_active=True,
    )

    updated_jadwal = JadwalDto(
        id=1,
        hari="Selasa",
        jam_mulai=time(10, 0),
        jam_selesai=time(12, 0),
        ruangan="R102",
        mata_kuliah_id=2,
        dosen_id=2,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.update.return_value = updated_jadwal

    # Act
    result = jadwal_service.update(update_dto)

    # Assert
    assert result == updated_jadwal
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=1))
    mock_jadwal_repo.update.assert_called_once_with(update_dto)


def test_update_jadwal_not_found_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that updating a non-existent jadwal raises NotFoundException.
    """
    update_dto = UpdateJadwalDto(
        id=999,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal does not exist
    mock_jadwal_repo.read.return_value = []

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        jadwal_service.update(update_dto)

    assert "Jadwal" in str(exc_info.value)
    assert "999" in str(exc_info.value)
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=999))
    mock_jadwal_repo.update.assert_not_called()


def test_update_jadwal_invalid_time_range_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that updating jadwal with invalid time range raises InvalidInputException.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(12, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.update(update_dto)

    assert "Jam mulai must be before jam selesai" in str(exc_info.value)
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=1))
    mock_jadwal_repo.update.assert_not_called()


def test_update_jadwal_same_start_and_end_time_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that updating jadwal with same start and end time raises InvalidInputException.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(10, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal

    # Act & Assert
    with pytest.raises(InvalidInputException) as exc_info:
        jadwal_service.update(update_dto)

    assert "Jam mulai must be before jam selesai" in str(exc_info.value)
    mock_jadwal_repo.update.assert_not_called()


def test_update_jadwal_change_only_hari(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test updating only the hari field of a jadwal.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Rabu",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    updated_jadwal = JadwalDto(
        id=1,
        hari="Rabu",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.update.return_value = updated_jadwal

    # Act
    result = jadwal_service.update(update_dto)

    # Assert
    assert result.hari == "Rabu"
    assert result.jam_mulai == time(8, 0)
    mock_jadwal_repo.update.assert_called_once_with(update_dto)


def test_update_jadwal_change_only_ruangan(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test updating only the ruangan field of a jadwal.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R201",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    updated_jadwal = JadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R201",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.update.return_value = updated_jadwal

    # Act
    result = jadwal_service.update(update_dto)

    # Assert
    assert result.ruangan == "R201"
    mock_jadwal_repo.update.assert_called_once_with(update_dto)


def test_update_jadwal_change_time_range(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test updating the time range of a jadwal.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(13, 0),
        jam_selesai=time(15, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    updated_jadwal = JadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(13, 0),
        jam_selesai=time(15, 0),
        ruangan="R101",
        mata_kuliah_id=1,
        dosen_id=1,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.update.return_value = updated_jadwal

    # Act
    result = jadwal_service.update(update_dto)

    # Assert
    assert result.jam_mulai == time(13, 0)
    assert result.jam_selesai == time(15, 0)
    mock_jadwal_repo.update.assert_called_once_with(update_dto)


def test_update_jadwal_change_mata_kuliah_and_dosen(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test updating mata_kuliah_id and dosen_id of a jadwal.
    """
    existing_jadwal = [
        JadwalDto(
            id=1,
            hari="Senin",
            jam_mulai=time(8, 0),
            jam_selesai=time(10, 0),
            ruangan="R101",
            mata_kuliah_id=1,
            dosen_id=1,
            is_active=True,
        )
    ]

    update_dto = UpdateJadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=3,
        dosen_id=3,
        is_active=True,
    )

    updated_jadwal = JadwalDto(
        id=1,
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="R101",
        mata_kuliah_id=3,
        dosen_id=3,
        is_active=True,
    )

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.update.return_value = updated_jadwal

    # Act
    result = jadwal_service.update(update_dto)

    # Assert
    assert result.mata_kuliah_id == 3
    assert result.dosen_id == 3
    mock_jadwal_repo.update.assert_called_once_with(update_dto)

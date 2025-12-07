from datetime import time
from unittest.mock import MagicMock

import pytest

from src.application.dtos.jadwal_dto import JadwalDto
from src.application.exceptions import NotFoundException
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


def test_delete_jadwal_success(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test deleting an existing jadwal successfully.
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
        )
    ]

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.delete.return_value = True

    # Act
    result = jadwal_service.delete(jadwal_id=1)

    # Assert
    assert result is True
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=1))
    mock_jadwal_repo.delete.assert_called_once_with(1)


def test_delete_jadwal_not_found_raises_exception(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that deleting a non-existent jadwal raises NotFoundException.
    """
    # Mock: jadwal does not exist
    mock_jadwal_repo.read.return_value = []

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        jadwal_service.delete(jadwal_id=999)

    assert "Jadwal" in str(exc_info.value)
    assert "999" in str(exc_info.value)
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=999))
    mock_jadwal_repo.delete.assert_not_called()


def test_delete_jadwal_with_zero_id_not_found(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that deleting jadwal with ID 0 raises NotFoundException.
    """
    # Mock: jadwal does not exist
    mock_jadwal_repo.read.return_value = []

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        jadwal_service.delete(jadwal_id=0)

    assert "Jadwal" in str(exc_info.value)
    mock_jadwal_repo.delete.assert_not_called()


def test_delete_jadwal_with_negative_id_not_found(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that deleting jadwal with negative ID raises NotFoundException.
    """
    # Mock: jadwal does not exist
    mock_jadwal_repo.read.return_value = []

    # Act & Assert
    with pytest.raises(NotFoundException) as exc_info:
        jadwal_service.delete(jadwal_id=-1)

    assert "Jadwal" in str(exc_info.value)
    mock_jadwal_repo.delete.assert_not_called()


def test_delete_jadwal_repository_returns_false(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test deleting jadwal when repository returns False.
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
        )
    ]

    # Mock: jadwal exists but deletion fails
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.delete.return_value = False

    # Act
    result = jadwal_service.delete(jadwal_id=1)

    # Assert
    assert result is False
    mock_jadwal_repo.read.assert_called_once_with(GetJadwalPort(id=1))
    mock_jadwal_repo.delete.assert_called_once_with(1)


def test_delete_multiple_jadwal_sequentially(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test deleting multiple jadwal records sequentially.
    """
    jadwal_ids = [1, 2, 3]

    for jadwal_id in jadwal_ids:
        existing_jadwal = [
            JadwalDto(
                id=jadwal_id,
                hari="Senin",
                jam_mulai=time(8, 0),
                jam_selesai=time(10, 0),
                ruangan=f"R{jadwal_id}01",
                mata_kuliah_id=jadwal_id,
                dosen_id=jadwal_id,
            )
        ]

        mock_jadwal_repo.read.return_value = existing_jadwal
        mock_jadwal_repo.delete.return_value = True

        # Act
        result = jadwal_service.delete(jadwal_id=jadwal_id)

        # Assert
        assert result is True

    # Verify that delete was called for each jadwal_id
    assert mock_jadwal_repo.delete.call_count == len(jadwal_ids)


def test_delete_jadwal_verified_existence_check(
    jadwal_service: JadwalService, mock_jadwal_repo: MagicMock
):
    """
    Test that delete method checks for jadwal existence before deletion.
    """
    existing_jadwal = [
        JadwalDto(
            id=5,
            hari="Jumat",
            jam_mulai=time(14, 0),
            jam_selesai=time(16, 0),
            ruangan="R105",
            mata_kuliah_id=5,
            dosen_id=5,
        )
    ]

    # Mock: jadwal exists
    mock_jadwal_repo.read.return_value = existing_jadwal
    mock_jadwal_repo.delete.return_value = True

    # Act
    result = jadwal_service.delete(jadwal_id=5)

    # Assert
    assert result is True
    # Verify that read was called before delete
    assert mock_jadwal_repo.read.call_count == 1
    assert mock_jadwal_repo.delete.call_count == 1
    # Verify the order of calls
    assert mock_jadwal_repo.method_calls[0][0] == "read"
    assert mock_jadwal_repo.method_calls[1][0] == "delete"

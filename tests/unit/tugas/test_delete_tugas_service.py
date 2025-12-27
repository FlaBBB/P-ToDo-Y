from datetime import datetime
from unittest.mock import MagicMock
import warnings

import pytest

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

from src.application.dtos.tugas_dto import StatusTugas, TugasDto
from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.tugas_repository import (
    TugasRepositoryInterface,
)
from src.application.usecases.tugas import TugasService
from src.ports.tugas import GetTugasPort


@pytest.fixture
def mock_tugas_repo() -> MagicMock:
    """Fixture for a mocked TugasRepositoryInterface."""
    return MagicMock(spec=TugasRepositoryInterface)


@pytest.fixture
def tugas_service(mock_tugas_repo: MagicMock) -> TugasService:
    """Fixture for TugasService with a mocked repository."""
    return TugasService(tugas_repo=mock_tugas_repo)


def test_delete_tugas_success(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas successfully.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas UAS",
            deskripsi="Membuat aplikasi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    # Mock: Tugas exists
    mock_tugas_repo.read.return_value = existing_tugas
    # Mock: Delete returns True
    mock_tugas_repo.delete.return_value = True

    result = tugas_service.delete(tugas_id=1)

    # Verify repository was called to check if tugas exists
    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=1))
    # Verify repository was called to delete
    mock_tugas_repo.delete.assert_called_once_with(1)
    # Verify result
    assert result is True


def test_delete_tugas_not_found(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a non-existent Tugas raises NotFoundException.
    """
    # Mock: Tugas doesn't exist
    mock_tugas_repo.read.return_value = []

    with pytest.raises(NotFoundException) as exc_info:
        tugas_service.delete(tugas_id=999)

    assert "tugas" in str(exc_info.value).lower()
    assert "999" in str(exc_info.value)

    # Verify repository was called to check if tugas exists
    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=999))
    # Verify delete was never called
    mock_tugas_repo.delete.assert_not_called()


def test_delete_tugas_by_valid_id(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas with a valid ID.
    """
    existing_tugas = [
        TugasDto(
            id=5,
            judul="Tugas Valid",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.delete.return_value = True

    result = tugas_service.delete(tugas_id=5)

    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=5))
    mock_tugas_repo.delete.assert_called_once_with(5)
    assert result is True


def test_delete_tugas_with_mata_kuliah(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas that has mata_kuliah_id.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Pemrograman",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=5,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.delete.return_value = True

    result = tugas_service.delete(tugas_id=1)

    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=1))
    mock_tugas_repo.delete.assert_called_once_with(1)
    assert result is True


def test_delete_tugas_with_mahasiswa(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas that has mahasiswa_id.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas John",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=10,
        )
    ]

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.delete.return_value = True

    result = tugas_service.delete(tugas_id=1)

    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=1))
    mock_tugas_repo.delete.assert_called_once_with(1)
    assert result is True


def test_delete_tugas_with_all_relations(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas that has both mata_kuliah_id and mahasiswa_id.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Kompleks",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=3,
            mahasiswa_id=7,
        )
    ]

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.delete.return_value = True

    result = tugas_service.delete(tugas_id=1)

    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=1))
    mock_tugas_repo.delete.assert_called_once_with(1)
    assert result is True


def test_delete_tugas_different_statuses(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting Tugas with different statuses.
    """
    statuses = [
        StatusTugas.PENDING,
        StatusTugas.IN_PROGRESS,
        StatusTugas.DONE,
        StatusTugas.CANCELLED,
    ]

    for idx, status in enumerate(statuses, start=1):
        existing_tugas = [
            TugasDto(
                id=idx,
                judul=f"Tugas {status}",
                deskripsi="Deskripsi",
                deadline=datetime(2025, 12, 31, 23, 59, 59),
                status=status,
                mata_kuliah_id=None,
                mahasiswa_id=None,
            )
        ]

        mock_tugas_repo.read.return_value = existing_tugas
        mock_tugas_repo.delete.return_value = True

        result = tugas_service.delete(tugas_id=idx)

        assert result is True


def test_delete_tugas_multiple_calls(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting multiple Tugas one by one.
    """
    # First delete
    existing_tugas_1 = [
        TugasDto(
            id=1,
            judul="Tugas 1",
            deskripsi="Deskripsi 1",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]
    mock_tugas_repo.read.return_value = existing_tugas_1
    mock_tugas_repo.delete.return_value = True

    result1 = tugas_service.delete(tugas_id=1)
    assert result1 is True

    # Second delete
    existing_tugas_2 = [
        TugasDto(
            id=2,
            judul="Tugas 2",
            deskripsi="Deskripsi 2",
            deadline=datetime(2025, 12, 30, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]
    mock_tugas_repo.read.return_value = existing_tugas_2
    mock_tugas_repo.delete.return_value = True

    result2 = tugas_service.delete(tugas_id=2)
    assert result2 is True

    # Verify delete was called twice
    assert mock_tugas_repo.delete.call_count == 2


def test_delete_tugas_repository_returns_false(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test deleting a Tugas when repository returns False.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.delete.return_value = False

    result = tugas_service.delete(tugas_id=1)

    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=1))
    mock_tugas_repo.delete.assert_called_once_with(1)
    assert result is False

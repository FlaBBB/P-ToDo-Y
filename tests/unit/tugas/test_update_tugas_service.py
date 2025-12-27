from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.application.dtos.tugas_dto import StatusTugas, TugasDto, UpdateTugasDto
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


def test_update_tugas_success(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test updating a Tugas successfully.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Lama",
            deskripsi="Deskripsi lama",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas Baru",
        deskripsi="Deskripsi baru",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status=StatusTugas.IN_PROGRESS,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Baru",
        deskripsi="Deskripsi baru",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status=StatusTugas.IN_PROGRESS,
        mata_kuliah_id=None,
        mahasiswa_id=None,
    )

    # Mock: Tugas exists
    mock_tugas_repo.read.return_value = existing_tugas
    # Mock: Update returns the updated tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    # Verify repository was called to check if tugas exists
    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=update_dto.id))
    # Verify repository was called to update
    mock_tugas_repo.update.assert_called_once_with(update_dto)
    # Verify result
    assert result == expected_result
    assert result.judul == "Tugas Baru"
    assert result.status == StatusTugas.IN_PROGRESS


def test_update_tugas_not_found(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test updating a non-existent Tugas raises NotFoundException.
    """
    update_dto = UpdateTugasDto(
        id=999,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
    )

    # Mock: Tugas doesn't exist
    mock_tugas_repo.read.return_value = []

    with pytest.raises(NotFoundException) as exc_info:
        tugas_service.update(update_dto)

    assert "tugas" in str(exc_info.value).lower()
    assert "999" in str(exc_info.value)

    # Verify repository was called to check if tugas exists
    mock_tugas_repo.read.assert_called_once_with(GetTugasPort(id=999))
    # Verify update was never called
    mock_tugas_repo.update.assert_not_called()


def test_update_tugas_change_status(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test updating Tugas status from pending to done.
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

    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.DONE,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.DONE,
        mata_kuliah_id=None,
        mahasiswa_id=None,
    )

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    assert result.status == StatusTugas.DONE


def test_update_tugas_add_mata_kuliah(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test adding mata_kuliah_id to an existing Tugas.
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

    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=5,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=5,
        mahasiswa_id=None,
    )

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    assert result.mata_kuliah_id == 5


def test_update_tugas_add_mahasiswa(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test adding mahasiswa_id to an existing Tugas.
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

    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mahasiswa_id=10,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=None,
        mahasiswa_id=10,
    )

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    assert result.mahasiswa_id == 10


def test_update_tugas_change_deadline(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test updating Tugas deadline.
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

    new_deadline = datetime(2026, 1, 15, 23, 59, 59)
    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=new_deadline,
        status=StatusTugas.PENDING,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=new_deadline,
        status=StatusTugas.PENDING,
        mata_kuliah_id=None,
        mahasiswa_id=None,
    )

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    assert result.deadline == new_deadline


def test_update_tugas_all_status_transitions(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test transitioning through all status states.
    """
    statuses = [
        StatusTugas.PENDING,
        StatusTugas.IN_PROGRESS,
        StatusTugas.DONE,
        StatusTugas.CANCELLED,
    ]

    for status in statuses:
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

        update_dto = UpdateTugasDto(
            id=1,
            judul="Tugas",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=status,
        )

        expected_result = TugasDto(
            id=1,
            judul="Tugas",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=status,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )

        mock_tugas_repo.read.return_value = existing_tugas
        mock_tugas_repo.update.return_value = expected_result

        result = tugas_service.update(update_dto)

        assert result.status == status


def test_update_tugas_change_all_fields(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test updating all fields of a Tugas.
    """
    existing_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Lama",
            deskripsi="Deskripsi lama",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=1,
            mahasiswa_id=1,
        )
    ]

    update_dto = UpdateTugasDto(
        id=1,
        judul="Tugas Baru",
        deskripsi="Deskripsi baru",
        deadline=datetime(2026, 1, 15, 23, 59, 59),
        status=StatusTugas.IN_PROGRESS,
        mata_kuliah_id=2,
        mahasiswa_id=2,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Baru",
        deskripsi="Deskripsi baru",
        deadline=datetime(2026, 1, 15, 23, 59, 59),
        status=StatusTugas.IN_PROGRESS,
        mata_kuliah_id=2,
        mahasiswa_id=2,
    )

    mock_tugas_repo.read.return_value = existing_tugas
    mock_tugas_repo.update.return_value = expected_result

    result = tugas_service.update(update_dto)

    assert result.judul == "Tugas Baru"
    assert result.deskripsi == "Deskripsi baru"
    assert result.status == StatusTugas.IN_PROGRESS
    assert result.mata_kuliah_id == 2
    assert result.mahasiswa_id == 2

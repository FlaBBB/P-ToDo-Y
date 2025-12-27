from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.application.dtos.tugas_dto import CreateTugasDto, StatusTugas, TugasDto
from src.application.exceptions import InvalidInputException
from src.application.usecases.interfaces.tugas_repository import (
    TugasRepositoryInterface,
)
from src.application.usecases.tugas import TugasService


@pytest.fixture
def mock_tugas_repo() -> MagicMock:
    """Fixture for a mocked TugasRepositoryInterface."""
    return MagicMock(spec=TugasRepositoryInterface)


@pytest.fixture
def tugas_service(mock_tugas_repo: MagicMock) -> TugasService:
    """Fixture for TugasService with a mocked repository."""
    return TugasService(tugas_repo=mock_tugas_repo)


def test_create_tugas_success(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a new Tugas successfully.
    """
    create_dto = CreateTugasDto(
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi web dengan FastAPI",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=1,
        mahasiswa_id=1,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi web dengan FastAPI",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=1,
        mahasiswa_id=1,
    )

    # Mock: Create returns the new tugas
    mock_tugas_repo.create.return_value = expected_result

    result = tugas_service.create(create_dto)

    # Verify repository was called to create
    mock_tugas_repo.create.assert_called_once_with(create_dto)
    # Verify result
    assert result == expected_result
    assert result.judul == "Tugas UAS"
    assert result.status == StatusTugas.PENDING


def test_create_tugas_minimal(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a Tugas with minimal required fields.
    """
    create_dto = CreateTugasDto(
        judul="Tugas Mingguan",
        deskripsi="Latihan soal",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Mingguan",
        deskripsi="Latihan soal",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=None,
        mahasiswa_id=None,
    )

    mock_tugas_repo.create.return_value = expected_result

    result = tugas_service.create(create_dto)

    mock_tugas_repo.create.assert_called_once_with(create_dto)
    assert result == expected_result
    assert result.mata_kuliah_id is None
    assert result.mahasiswa_id is None


def test_create_tugas_empty_judul(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a Tugas with empty judul raises InvalidInputException.
    """
    create_dto = CreateTugasDto(
        judul="",  # Empty judul
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
    )

    with pytest.raises(InvalidInputException) as exc_info:
        tugas_service.create(create_dto)

    assert "judul" in str(exc_info.value).lower()
    # Verify create was never called
    mock_tugas_repo.create.assert_not_called()


def test_create_tugas_with_mata_kuliah(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a Tugas with mata_kuliah_id.
    """
    create_dto = CreateTugasDto(
        judul="Tugas Pemrograman",
        deskripsi="Membuat API",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=5,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Pemrograman",
        deskripsi="Membuat API",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=5,
        mahasiswa_id=None,
    )

    mock_tugas_repo.create.return_value = expected_result

    result = tugas_service.create(create_dto)

    mock_tugas_repo.create.assert_called_once_with(create_dto)
    assert result.mata_kuliah_id == 5


def test_create_tugas_with_mahasiswa(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a Tugas with mahasiswa_id.
    """
    create_dto = CreateTugasDto(
        judul="Tugas Personal",
        deskripsi="Tugas individu",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mahasiswa_id=10,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Personal",
        deskripsi="Tugas individu",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=None,
        mahasiswa_id=10,
    )

    mock_tugas_repo.create.return_value = expected_result

    result = tugas_service.create(create_dto)

    mock_tugas_repo.create.assert_called_once_with(create_dto)
    assert result.mahasiswa_id == 10


def test_create_tugas_with_all_statuses(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating Tugas with different status types.
    """
    statuses = [
        StatusTugas.PENDING,
        StatusTugas.IN_PROGRESS,
        StatusTugas.DONE,
        StatusTugas.CANCELLED,
    ]

    for idx, status in enumerate(statuses, start=1):
        create_dto = CreateTugasDto(
            judul=f"Tugas {status}",
            deskripsi="Test tugas",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=status,
        )

        expected_result = TugasDto(
            id=idx,
            judul=f"Tugas {status}",
            deskripsi="Test tugas",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=status,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )

        mock_tugas_repo.create.return_value = expected_result

        result = tugas_service.create(create_dto)

        assert result.status == status


def test_create_tugas_with_both_relations(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test creating a Tugas with both mata_kuliah_id and mahasiswa_id.
    """
    create_dto = CreateTugasDto(
        judul="Tugas Kompleks",
        deskripsi="Tugas dengan semua relasi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=3,
        mahasiswa_id=7,
    )

    expected_result = TugasDto(
        id=1,
        judul="Tugas Kompleks",
        deskripsi="Tugas dengan semua relasi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status=StatusTugas.PENDING,
        mata_kuliah_id=3,
        mahasiswa_id=7,
    )

    mock_tugas_repo.create.return_value = expected_result

    result = tugas_service.create(create_dto)

    mock_tugas_repo.create.assert_called_once_with(create_dto)
    assert result.mata_kuliah_id == 3
    assert result.mahasiswa_id == 7

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.application.dtos.tugas_dto import StatusTugas, TugasDto
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


def test_read_all_tugas(tugas_service: TugasService, mock_tugas_repo: MagicMock):
    """
    Test reading all Tugas records.
    """
    expected_tugas_list = [
        TugasDto(
            id=1,
            judul="Tugas 1",
            deskripsi="Deskripsi 1",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        ),
        TugasDto(
            id=2,
            judul="Tugas 2",
            deskripsi="Deskripsi 2",
            deadline=datetime(2025, 12, 30, 23, 59, 59),
            status=StatusTugas.IN_PROGRESS,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        ),
    ]

    mock_tugas_repo.read.return_value = expected_tugas_list

    get_tugas_port = GetTugasPort()
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert result == expected_tugas_list
    assert len(result) == 2


def test_read_tugas_by_id(tugas_service: TugasService, mock_tugas_repo: MagicMock):
    """
    Test reading a Tugas by ID.
    """
    expected_tugas = [
        TugasDto(
            id=1,
            judul="Tugas UAS",
            deskripsi="Membuat aplikasi web",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(id=1)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert result == expected_tugas
    assert len(result) == 1
    assert result[0].id == 1


def test_read_tugas_by_judul(tugas_service: TugasService, mock_tugas_repo: MagicMock):
    """
    Test reading Tugas by judul.
    """
    expected_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Pemrograman",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(judul="Pemrograman")
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 1
    assert "Pemrograman" in result[0].judul


def test_read_tugas_by_status(tugas_service: TugasService, mock_tugas_repo: MagicMock):
    """
    Test reading Tugas by status.
    """
    expected_tugas = [
        TugasDto(
            id=1,
            judul="Tugas 1",
            deskripsi="Deskripsi 1",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        ),
        TugasDto(
            id=2,
            judul="Tugas 2",
            deskripsi="Deskripsi 2",
            deadline=datetime(2025, 12, 30, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=None,
            mahasiswa_id=None,
        ),
    ]

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(status=StatusTugas.PENDING)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 2
    assert all(t.status == StatusTugas.PENDING for t in result)


def test_read_tugas_by_mata_kuliah_id(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test reading Tugas by mata_kuliah_id.
    """
    expected_tugas = [
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

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(mata_kuliah_id=5)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 1
    assert result[0].mata_kuliah_id == 5


def test_read_tugas_by_mahasiswa_id(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test reading Tugas by mahasiswa_id.
    """
    expected_tugas = [
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

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(mahasiswa_id=10)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 1
    assert result[0].mahasiswa_id == 10


def test_read_tugas_not_found(tugas_service: TugasService, mock_tugas_repo: MagicMock):
    """
    Test reading a non-existent Tugas returns empty list.
    """
    mock_tugas_repo.read.return_value = []

    get_tugas_port = GetTugasPort(id=999)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert result == []
    assert len(result) == 0


def test_read_tugas_empty_database(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test reading from empty database returns empty list.
    """
    mock_tugas_repo.read.return_value = []

    get_tugas_port = GetTugasPort()
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert result == []


def test_read_tugas_multiple_filters(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test reading Tugas with multiple filters.
    """
    expected_tugas = [
        TugasDto(
            id=1,
            judul="Tugas 1",
            deskripsi="Deskripsi 1",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.PENDING,
            mata_kuliah_id=3,
            mahasiswa_id=None,
        )
    ]

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(mata_kuliah_id=3, status=StatusTugas.PENDING)
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 1
    assert result[0].mata_kuliah_id == 3
    assert result[0].status == StatusTugas.PENDING


def test_read_tugas_by_all_filters(
    tugas_service: TugasService, mock_tugas_repo: MagicMock
):
    """
    Test reading Tugas with all possible filters.
    """
    expected_tugas = [
        TugasDto(
            id=1,
            judul="Tugas Spesifik",
            deskripsi="Deskripsi",
            deadline=datetime(2025, 12, 31, 23, 59, 59),
            status=StatusTugas.IN_PROGRESS,
            mata_kuliah_id=5,
            mahasiswa_id=10,
        )
    ]

    mock_tugas_repo.read.return_value = expected_tugas

    get_tugas_port = GetTugasPort(
        id=1,
        judul="Spesifik",
        status=StatusTugas.IN_PROGRESS,
        mata_kuliah_id=5,
        mahasiswa_id=10,
    )
    result = tugas_service.read(get_tugas_port)

    mock_tugas_repo.read.assert_called_once_with(get_tugas_port)
    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].mata_kuliah_id == 5
    assert result[0].mahasiswa_id == 10

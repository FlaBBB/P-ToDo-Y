from unittest.mock import MagicMock

import pytest

from src.application.dtos.dosen_dto import DosenDto
from src.application.enums import DosenStatus
from src.application.usecases.interfaces.dosen_repository import (
    DosenRepositoryInterface,
)
from src.application.usecases.dosen import DosenService
from src.ports.dosen import GetDosenPort


@pytest.fixture
def mock_dosen_repo() -> MagicMock:
    """Fixture for a mocked DosenRepositoryInterface."""
    return MagicMock(spec=DosenRepositoryInterface)


@pytest.fixture
def dosen_service(mock_dosen_repo: MagicMock) -> DosenService:
    """Fixture for DosenService with a mocked repository."""
    return DosenService(dosen_repo=mock_dosen_repo)


def test_read_all_dosen(dosen_service: DosenService, mock_dosen_repo: MagicMock):
    """
    Test reading all Dosen records.
    """
    expected_dosen_list = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Prof. Jane Smith",
            email="jane.smith@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
    ]

    mock_dosen_repo.read.return_value = expected_dosen_list

    get_dosen_port = GetDosenPort()
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen_list
    assert len(result) == 2


def test_read_dosen_by_id(dosen_service: DosenService, mock_dosen_repo: MagicMock):
    """
    Test reading a Dosen by ID.
    """
    expected_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    mock_dosen_repo.read.return_value = expected_dosen

    get_dosen_port = GetDosenPort(id=1)
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen
    assert len(result) == 1
    assert result[0].id == 1


def test_read_dosen_by_nidn(dosen_service: DosenService, mock_dosen_repo: MagicMock):
    """
    Test reading a Dosen by NIDN.
    """
    expected_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    mock_dosen_repo.read.return_value = expected_dosen

    get_dosen_port = GetDosenPort(nidn="0123456789")
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen
    assert result[0].nidn == "0123456789"


def test_read_dosen_by_nama(dosen_service: DosenService, mock_dosen_repo: MagicMock):
    """
    Test reading Dosen by nama (partial match).
    """
    expected_dosen_list = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
        DosenDto(
            id=2,
            nidn="1111111111",
            nama="Dr. John Smith",
            email="john.smith@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
    ]

    mock_dosen_repo.read.return_value = expected_dosen_list

    get_dosen_port = GetDosenPort(nama="John")
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert len(result) == 2
    assert all("John" in dosen.nama for dosen in result)


def test_read_dosen_by_email(dosen_service: DosenService, mock_dosen_repo: MagicMock):
    """
    Test reading a Dosen by email.
    """
    expected_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    mock_dosen_repo.read.return_value = expected_dosen

    get_dosen_port = GetDosenPort(email="john.doe@university.ac.id")
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen
    assert result[0].email == "john.doe@university.ac.id"


def test_read_dosen_with_pagination(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test reading Dosen with pagination.
    """
    expected_dosen_list = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Prof. Jane Smith",
            email="jane.smith@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
    ]

    mock_dosen_repo.read.return_value = expected_dosen_list

    get_dosen_port = GetDosenPort(limit=2, page=1)
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert len(result) == 2


def test_read_dosen_with_ordering(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test reading Dosen with ordering.
    """
    expected_dosen_list = [
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Prof. Jane Smith",
            email="jane.smith@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        ),
    ]

    mock_dosen_repo.read.return_value = expected_dosen_list

    get_dosen_port = GetDosenPort(order_by="nama", order="desc")
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen_list


def test_read_dosen_not_found(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test reading Dosen when no records match the criteria.
    """
    mock_dosen_repo.read.return_value = []

    get_dosen_port = GetDosenPort(id=999)
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == []
    assert len(result) == 0


def test_read_dosen_multiple_filters(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test reading Dosen with multiple filters.
    """
    expected_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    mock_dosen_repo.read.return_value = expected_dosen

    get_dosen_port = GetDosenPort(nidn="0123456789", nama="John")
    result = dosen_service.read(get_dosen_port)

    mock_dosen_repo.read.assert_called_once_with(get_dosen_port)
    assert result == expected_dosen

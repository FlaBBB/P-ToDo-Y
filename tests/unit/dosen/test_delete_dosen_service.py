from unittest.mock import MagicMock

import pytest

from src.application.dtos.dosen_dto import DosenDto
from src.application.enums import DosenStatus
from src.application.exceptions import NotFoundException
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


def test_delete_dosen_success(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test deleting a Dosen successfully.
    """
    existing_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Delete returns True
    mock_dosen_repo.delete.return_value = True

    result = dosen_service.delete(dosen_id=1)

    # Verify repository was called to check if dosen exists
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=1))
    # Verify repository was called to delete
    mock_dosen_repo.delete.assert_called_once_with(1)
    # Verify result
    assert result is True


def test_delete_dosen_not_found(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test deleting a non-existent Dosen raises NotFoundException.
    """
    # Mock: Dosen doesn't exist
    mock_dosen_repo.read.return_value = []

    with pytest.raises(NotFoundException) as exc_info:
        dosen_service.delete(dosen_id=999)

    assert "dosen" in str(exc_info.value).lower()
    assert "999" in str(exc_info.value)

    # Verify repository was called to check if dosen exists
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=999))
    # Verify delete was never called
    mock_dosen_repo.delete.assert_not_called()


def test_delete_dosen_by_valid_id(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test deleting a Dosen with a valid ID.
    """
    existing_dosen = [
        DosenDto(
            id=5,
            nidn="5555555555",
            nama="Dr. Test Dosen",
            email="test.dosen@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Delete returns True
    mock_dosen_repo.delete.return_value = True

    result = dosen_service.delete(dosen_id=5)

    # Verify correct ID was used
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=5))
    mock_dosen_repo.delete.assert_called_once_with(5)
    assert result is True


def test_delete_dosen_returns_false(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test deleting a Dosen when repository returns False.
    This could happen if the database operation fails.
    """
    existing_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. John Doe",
            email="john.doe@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Delete returns False (operation failed)
    mock_dosen_repo.delete.return_value = False

    result = dosen_service.delete(dosen_id=1)

    # Verify repository was called
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=1))
    mock_dosen_repo.delete.assert_called_once_with(1)
    # Verify result is False
    assert result is False

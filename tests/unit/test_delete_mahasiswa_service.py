from unittest.mock import MagicMock

import pytest

from src.application.exceptions import NotFoundException
from src.application.usecases.interfaces.mahasiswa_repository import (
    MahasiswaRepositoryInterface,
)
from src.application.usecases.mahasiswa import MahasiswaService


@pytest.fixture
def mock_mahasiswa_repo() -> MagicMock:
    """Fixture for a mocked MahasiswaRepositoryInterface."""
    return MagicMock(spec=MahasiswaRepositoryInterface)


@pytest.fixture
def mahasiswa_service(mock_mahasiswa_repo: MagicMock) -> MahasiswaService:
    """Fixture for MahasiswaService with a mocked repository."""
    return MahasiswaService(mahasiswa_repo=mock_mahasiswa_repo)


def test_delete_mahasiswa_success(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test deleting a Mahasiswa successfully.
    """
    mahasiswa_id = 1
    mock_mahasiswa_repo.delete.return_value = True

    result = mahasiswa_service.delete(mahasiswa_id)

    mock_mahasiswa_repo.delete.assert_called_once_with(mahasiswa_id)
    assert result is True


def test_delete_mahasiswa_not_found(
    mahasiswa_service: MahasiswaService, mock_mahasiswa_repo: MagicMock
):
    """
    Test deleting a non-existent Mahasiswa raises NotFoundException.
    """
    mahasiswa_id = 999
    mock_mahasiswa_repo.delete.side_effect = NotFoundException(
        resource_name="Mahasiswa", identifier=mahasiswa_id
    )

    with pytest.raises(NotFoundException) as exc_info:
        mahasiswa_service.delete(mahasiswa_id)

    assert "Mahasiswa with ID/NIM '999' not found" in str(exc_info.value.message)
    mock_mahasiswa_repo.delete.assert_called_once_with(mahasiswa_id)

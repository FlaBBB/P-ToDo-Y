from unittest.mock import MagicMock

import pytest

from src.application.dtos.dosen_dto import DosenDto, UpdateDosenDto
from src.application.enums import DosenStatus
from src.application.exceptions import DuplicateEntryException, NotFoundException
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


def test_update_dosen_success(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a Dosen successfully.
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

    update_dto = UpdateDosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe Updated",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    expected_result = DosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe Updated",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Update returns the updated dosen
    mock_dosen_repo.update.return_value = expected_result

    result = dosen_service.update(update_dto)

    # Verify repository was called to check if dosen exists
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=update_dto.id))
    # Verify repository was called to update
    mock_dosen_repo.update.assert_called_once_with(update_dto)
    # Verify result
    assert result == expected_result
    assert result.nama == "Dr. John Doe Updated"


def test_update_dosen_not_found(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a non-existent Dosen raises NotFoundException.
    """
    update_dto = UpdateDosenDto(
        id=999,
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: Dosen doesn't exist
    mock_dosen_repo.read.return_value = []

    with pytest.raises(NotFoundException) as exc_info:
        dosen_service.update(update_dto)

    assert "dosen" in str(exc_info.value).lower()
    assert "999" in str(exc_info.value)

    # Verify repository was called to check if dosen exists
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=update_dto.id))
    # Verify update was never called
    mock_dosen_repo.update.assert_not_called()


def test_update_dosen_change_nidn_to_existing(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a Dosen's NIDN to one that already exists raises DuplicateEntryException.
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

    another_dosen_with_new_nidn = [
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Dr. Another Dosen",
            email="another@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    update_dto = UpdateDosenDto(
        id=1,
        nidn="9876543210",  # Trying to change to an existing NIDN
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: First call returns existing dosen, second call returns dosen with duplicate NIDN
    mock_dosen_repo.read.side_effect = [existing_dosen, another_dosen_with_new_nidn]

    with pytest.raises(DuplicateEntryException) as exc_info:
        dosen_service.update(update_dto)

    assert "nidn" in str(exc_info.value).lower()
    assert "already exists" in str(exc_info.value).lower()

    # Verify repository was called twice
    assert mock_dosen_repo.read.call_count == 2
    # Verify update was never called
    mock_dosen_repo.update.assert_not_called()


def test_update_dosen_change_email_to_existing(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a Dosen's email to one that already exists raises DuplicateEntryException.
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

    another_dosen_with_new_email = [
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Dr. Another Dosen",
            email="duplicate@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    update_dto = UpdateDosenDto(
        id=1,
        nidn="0123456789",  # Same NIDN, so NIDN check is skipped
        nama="Dr. John Doe",
        email="duplicate@university.ac.id",  # Trying to change to an existing email
        status=DosenStatus.ACTIVE,
    )

    # Mock: First call returns existing dosen, second call returns dosen with duplicate email
    mock_dosen_repo.read.side_effect = [
        existing_dosen,  # Check if dosen exists
        another_dosen_with_new_email,  # Email check fails
    ]

    with pytest.raises(DuplicateEntryException) as exc_info:
        dosen_service.update(update_dto)

    assert "email" in str(exc_info.value).lower()
    assert "already exists" in str(exc_info.value).lower()

    # Verify repository was called twice
    assert mock_dosen_repo.read.call_count == 2
    # Verify update was never called
    mock_dosen_repo.update.assert_not_called()
def test_update_dosen_change_status(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a Dosen's status.
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

    update_dto = UpdateDosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.LEAVE,  # Changing status to LEAVE
    )

    expected_result = DosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.LEAVE,
    )

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Update returns the updated dosen
    mock_dosen_repo.update.return_value = expected_result

    result = dosen_service.update(update_dto)

    assert result.status == DosenStatus.LEAVE
    mock_dosen_repo.update.assert_called_once_with(update_dto)


def test_update_dosen_no_changes(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test updating a Dosen with no changes to NIDN or email.
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

    update_dto = UpdateDosenDto(
        id=1,
        nidn="0123456789",  # Same NIDN
        nama="Dr. John Doe Updated",
        email="john.doe@university.ac.id",  # Same email
        status=DosenStatus.ACTIVE,
    )

    expected_result = DosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe Updated",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: Dosen exists
    mock_dosen_repo.read.return_value = existing_dosen
    # Mock: Update returns the updated dosen
    mock_dosen_repo.update.return_value = expected_result

    result = dosen_service.update(update_dto)

    # When NIDN and email don't change, only one read call is made
    mock_dosen_repo.read.assert_called_once_with(GetDosenPort(id=update_dto.id))
    mock_dosen_repo.update.assert_called_once_with(update_dto)
    assert result.nama == "Dr. John Doe Updated"

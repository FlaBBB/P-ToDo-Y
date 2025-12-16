from unittest.mock import MagicMock


from src.application.dtos.dosen_dto import CreateDosenDto, DosenDto
from src.application.enums import DosenStatus
from src.application.exceptions import DuplicateEntryException, InvalidInputException
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


def test_create_dosen_success(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a new Dosen successfully.
    """
    create_dto = CreateDosenDto(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    expected_result = DosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: NIDN doesn't exist yet
    mock_dosen_repo.read.side_effect = [[], []]  # First for NIDN, second for email
    # Mock: Create returns the new dosen
    mock_dosen_repo.create.return_value = expected_result

    result = dosen_service.create(create_dto)

    # Verify repository was called to check for existing NIDN
    assert mock_dosen_repo.read.call_count == 2
    mock_dosen_repo.read.assert_any_call(GetDosenPort(nidn=create_dto.nidn))
    mock_dosen_repo.read.assert_any_call(GetDosenPort(email=create_dto.email))
    # Verify repository was called to create
    mock_dosen_repo.create.assert_called_once_with(create_dto)
    # Verify result
    assert result == expected_result


def test_create_dosen_duplicate_nidn(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with a duplicate NIDN raises DuplicateEntryException.
    """
    create_dto = CreateDosenDto(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    existing_dosen = [
        DosenDto(
            id=1,
            nidn="0123456789",
            nama="Dr. Existing Dosen",
            email="existing@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    # Mock: NIDN already exists
    mock_dosen_repo.read.return_value = existing_dosen

    with pytest.raises(DuplicateEntryException) as exc_info:
        dosen_service.create(create_dto)

    assert "nidn" in str(exc_info.value).lower()
    assert "already exists" in str(exc_info.value).lower()

    # Verify repository was called to check for existing NIDN
    mock_dosen_repo.read.assert_called_once_with(
        GetDosenPort(nidn=create_dto.nidn)
    )
    # Verify create was never called
    mock_dosen_repo.create.assert_not_called()


def test_create_dosen_duplicate_email(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with a duplicate email raises DuplicateEntryException.
    """
    create_dto = CreateDosenDto(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="duplicate@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    existing_dosen_with_email = [
        DosenDto(
            id=2,
            nidn="9876543210",
            nama="Dr. Another Dosen",
            email="duplicate@university.ac.id",
            status=DosenStatus.ACTIVE,
        )
    ]

    # Mock: NIDN doesn't exist, but email already exists
    mock_dosen_repo.read.side_effect = [[], existing_dosen_with_email]

    with pytest.raises(DuplicateEntryException) as exc_info:
        dosen_service.create(create_dto)

    assert "email" in str(exc_info.value).lower()
    assert "already exists" in str(exc_info.value).lower()

    # Verify repository was called twice (NIDN check, email check)
    assert mock_dosen_repo.read.call_count == 2
    # Verify create was never called
    mock_dosen_repo.create.assert_not_called()


def test_create_dosen_invalid_nidn_empty(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with empty NIDN raises InvalidInputException.
    """
    create_dto = CreateDosenDto(
        nidn="",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    with pytest.raises(InvalidInputException) as exc_info:
        dosen_service.create(create_dto)

    assert "NIDN cannot be empty" in str(exc_info.value)
    # Verify repository was never called
    mock_dosen_repo.read.assert_not_called()
    mock_dosen_repo.create.assert_not_called()


def test_create_dosen_invalid_nama_empty(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with empty nama raises InvalidInputException.
    """
    create_dto = CreateDosenDto(
        nidn="0123456789",
        nama="",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    with pytest.raises(InvalidInputException) as exc_info:
        dosen_service.create(create_dto)

    assert "Nama cannot be empty" in str(exc_info.value)
    # Verify repository was never called
    mock_dosen_repo.read.assert_not_called()
    mock_dosen_repo.create.assert_not_called()


def test_create_dosen_invalid_email_empty(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with empty email raises Pydantic ValidationError.
    Note: Pydantic validates email format before it reaches the service layer.
    """
    from pydantic_core import ValidationError
    
    with pytest.raises(ValidationError):
        create_dto = CreateDosenDto(
            nidn="0123456789",
            nama="Dr. John Doe",
            email="",
            status=DosenStatus.ACTIVE,
        )


def test_create_dosen_default_status(
    dosen_service: DosenService, mock_dosen_repo: MagicMock
):
    """
    Test creating a Dosen with default status (ACTIVE).
    """
    create_dto = CreateDosenDto(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )

    expected_result = DosenDto(
        id=1,
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
        status=DosenStatus.ACTIVE,
    )

    # Mock: NIDN and email don't exist yet
    mock_dosen_repo.read.side_effect = [[], []]
    # Mock: Create returns the new dosen
    mock_dosen_repo.create.return_value = expected_result

    result = dosen_service.create(create_dto)

    # Verify the default status is ACTIVE
    assert create_dto.status == DosenStatus.ACTIVE
    assert result.status == DosenStatus.ACTIVE
    mock_dosen_repo.create.assert_called_once_with(create_dto)

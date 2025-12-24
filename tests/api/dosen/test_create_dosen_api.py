from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel


def test_create_dosen_success(client: TestClient, db_session: Session):
    """
    Test creating a new Dosen record successfully.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nidn"] == payload["nidn"]
    assert data["nama"] == payload["nama"]
    assert data["email"] == payload["email"]
    assert data["status"] == payload["status"]
    assert "id" in data


def test_create_dosen_duplicate_nidn(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with a duplicate NIDN returns 409 Conflict.
    """
    # Insert a dosen first
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. Existing Dosen",
        email="existing@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()

    # Try to create another dosen with the same NIDN
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_create_dosen_duplicate_email(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with a duplicate email returns 409 Conflict.
    """
    # Insert a dosen first
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. Existing Dosen",
        email="duplicate@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()

    # Try to create another dosen with the same email
    payload = {
        "nidn": "9876543210",
        "nama": "Dr. John Doe",
        "email": "duplicate@university.ac.id",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_create_dosen_invalid_nidn_empty(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with empty NIDN returns 422 Unprocessable Entity.
    """
    payload = {
        "nidn": "",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422
    assert "NIDN cannot be empty" in response.json()["detail"]


def test_create_dosen_invalid_nama_empty(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with empty nama returns 422 Unprocessable Entity.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422
    assert "Nama cannot be empty" in response.json()["detail"]


def test_create_dosen_invalid_email_empty(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with empty email returns 422 Unprocessable Entity.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422
    # Pydantic validation error for email format
    detail = response.json()["detail"]
    assert isinstance(detail, list)
    assert any("email" in str(err).lower() for err in detail)


def test_create_dosen_invalid_email_format(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with invalid email format returns 422 Unprocessable Entity.
    Pydantic validation should catch this.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "invalid-email-format",
        "status": "active",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422


def test_create_dosen_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test creating a Dosen without required fields returns 422 Unprocessable Entity.
    """
    payload = {
        "nidn": "0123456789",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422


def test_create_dosen_with_default_status(client: TestClient, db_session: Session):
    """
    Test creating a Dosen without status field uses default status (active).
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "active"


def test_create_dosen_with_inactive_status(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with inactive status.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "inactive",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "inactive"


def test_create_dosen_with_leave_status(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with leave status.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "leave",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "leave"


def test_create_dosen_with_invalid_status(client: TestClient, db_session: Session):
    """
    Test creating a Dosen with invalid status returns 422 Unprocessable Entity.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "invalid_status",
    }
    response = client.post("/dosen/", json=payload)
    assert response.status_code == 422

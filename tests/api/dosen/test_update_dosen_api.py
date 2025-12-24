from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel


def test_update_dosen_success(client: TestClient, db_session: Session):
    """
    Test updating a Dosen successfully.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe Updated",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == dosen.id
    assert data["nama"] == "Dr. John Doe Updated"
    assert data["nidn"] == "0123456789"


def test_update_dosen_not_found(client: TestClient, db_session: Session):
    """
    Test updating a non-existent Dosen returns 404 Not Found.
    """
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.put("/dosen/999", json=payload)
    assert response.status_code == 404


def test_update_dosen_change_nidn_to_existing(client: TestClient, db_session: Session):
    """
    Test updating a Dosen's NIDN to one that already exists returns 409 Conflict.
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Dr. Jane Smith",
        email="jane.smith@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()
    db_session.refresh(dosen1)

    # Try to update dosen1's NIDN to dosen2's NIDN
    payload = {
        "nidn": "9876543210",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "active",
    }
    response = client.put(f"/dosen/{dosen1.id}", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_update_dosen_change_email_to_existing(client: TestClient, db_session: Session):
    """
    Test updating a Dosen's email to one that already exists returns 409 Conflict.
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Dr. Jane Smith",
        email="jane.smith@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()
    db_session.refresh(dosen1)

    # Try to update dosen1's email to dosen2's email
    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "jane.smith@university.ac.id",
        "status": "active",
    }
    response = client.put(f"/dosen/{dosen1.id}", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_update_dosen_change_status(client: TestClient, db_session: Session):
    """
    Test updating a Dosen's status.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "leave",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "leave"


def test_update_dosen_change_multiple_fields(client: TestClient, db_session: Session):
    """
    Test updating multiple fields of a Dosen.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "1111111111",
        "nama": "Prof. John Doe Jr.",
        "email": "john.doe.jr@university.ac.id",
        "status": "inactive",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nidn"] == "1111111111"
    assert data["nama"] == "Prof. John Doe Jr."
    assert data["email"] == "john.doe.jr@university.ac.id"
    assert data["status"] == "inactive"


def test_update_dosen_invalid_email_format(client: TestClient, db_session: Session):
    """
    Test updating a Dosen with invalid email format returns 422 Unprocessable Entity.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "invalid-email-format",
        "status": "active",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 422


def test_update_dosen_invalid_status(client: TestClient, db_session: Session):
    """
    Test updating a Dosen with invalid status returns 422 Unprocessable Entity.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",
        "nama": "Dr. John Doe",
        "email": "john.doe@university.ac.id",
        "status": "invalid_status",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 422


def test_update_dosen_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test updating a Dosen without required fields returns 422 Unprocessable Entity.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 422


def test_update_dosen_keep_same_nidn_and_email(client: TestClient, db_session: Session):
    """
    Test updating a Dosen while keeping the same NIDN and email.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    payload = {
        "nidn": "0123456789",  # Same NIDN
        "nama": "Dr. John Doe Updated",
        "email": "john.doe@university.ac.id",  # Same email
        "status": "active",
    }
    response = client.put(f"/dosen/{dosen.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["nama"] == "Dr. John Doe Updated"

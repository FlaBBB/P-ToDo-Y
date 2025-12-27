from datetime import date

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.application.enums import MahasiswaStatus
from src.repositories.database.models.mahasiswa import MahasiswaModel


def test_update_mahasiswa_success(client: TestClient, db_session: Session):
    """
    Test updating a Mahasiswa successfully via API.
    """
    # Create a mahasiswa to update
    mahasiswa = MahasiswaModel(
        nim="2024000011",
        nama="Original Name",
        kelas="TI-1A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2003, 1, 1),
        status=MahasiswaStatus.ACTIVE,
    )
    db_session.add(mahasiswa)
    db_session.commit()
    db_session.refresh(mahasiswa)

    payload = {
        "nim": "2024000011",
        "nama": "Updated Name",
        "kelas": "TI-1B",
        "tempat_lahir": "Bandung",
        "tanggal_lahir": "2003-01-01",
        "status": "active",
    }

    response = client.put(f"/mahasiswa/{mahasiswa.id}", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == mahasiswa.id
    assert data["nama"] == "Updated Name"
    assert data["kelas"] == "TI-1B"
    assert data["tempat_lahir"] == "Bandung"


def test_update_mahasiswa_not_found(client: TestClient, db_session: Session):
    """
    Test updating a non-existent Mahasiswa returns 404.
    """
    payload = {
        "nim": "2024000012",
        "nama": "Updated Name",
        "kelas": "TI-1B",
        "tempat_lahir": "Bandung",
        "tanggal_lahir": "2003-01-01",
        "status": "active",
    }

    response = client.put("/mahasiswa/99999", json=payload)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_mahasiswa_invalid_input(client: TestClient, db_session: Session):
    """
    Test updating a Mahasiswa with invalid input (e.g. missing fields) returns 422.
    """
    # Create a mahasiswa to update
    mahasiswa = MahasiswaModel(
        nim="2024000013",
        nama="Original Name",
        kelas="TI-1A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2003, 1, 1),
        status=MahasiswaStatus.ACTIVE,
    )
    db_session.add(mahasiswa)
    db_session.commit()
    db_session.refresh(mahasiswa)

    # Missing required fields like nama, kelas, etc.
    payload = {
        "nim": "2024000013",
    }

    response = client.put(f"/mahasiswa/{mahasiswa.id}", json=payload)

    assert response.status_code == 422

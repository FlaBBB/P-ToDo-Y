from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.repositories.database.models.mahasiswa import MahasiswaModel


@pytest.fixture
def setup_mahasiswa_data(db_session: Session):
    """
    Fixture to set up initial Mahasiswa data in the test database.
    """
    mahasiswa1 = MahasiswaModel(
        nim="2023000001",
        nama="Alice Wonderland",
        kelas="TI-3E",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2000, 1, 15),
    )
    mahasiswa2 = MahasiswaModel(
        nim="2023000002",
        nama="Bob The Builder",
        kelas="SIB-5F",
        tempat_lahir="Bandung",
        tanggal_lahir=date(2001, 5, 20),
    )
    mahasiswa3 = MahasiswaModel(
        nim="2023000003",
        nama="Charlie Chaplin",
        kelas="TI-3E",
        tempat_lahir="Surabaya",
        tanggal_lahir=date(1999, 10, 1),
    )
    mahasiswa4 = MahasiswaModel(
        nim="2024000004",
        nama="David Copperfield",
        kelas="SIB-1A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2002, 3, 1),
    )
    db_session.add_all([mahasiswa1, mahasiswa2, mahasiswa3, mahasiswa4])
    db_session.commit()
    # Refresh to get IDs
    db_session.refresh(mahasiswa1)
    db_session.refresh(mahasiswa2)
    db_session.refresh(mahasiswa3)
    db_session.refresh(mahasiswa4)
    return mahasiswa1, mahasiswa2, mahasiswa3, mahasiswa4


def test_create_mahasiswa_success(client: TestClient, db_session: Session):
    """
    Test creating a new Mahasiswa record successfully.
    """
    new_mahasiswa = {
        "nim": "2025000005",
        "nama": "Eve Polastri",
        "kelas": "TI-3B",
        "tempat_lahir": "Semarang",
        "tanggal_lahir": "2001-12-25",
    }

    response = client.post("/mahasiswa/", json=new_mahasiswa)
    assert response.status_code == 201

    data = response.json()
    assert data["nim"] == new_mahasiswa["nim"]
    assert data["nama"] == new_mahasiswa["nama"]
    assert data["kelas"] == new_mahasiswa["kelas"]
    assert data["tempat_lahir"] == new_mahasiswa["tempat_lahir"]
    assert data["tanggal_lahir"] == new_mahasiswa["tanggal_lahir"]

    # pastikan data tersimpan di DB
    from src.repositories.database.models.mahasiswa import MahasiswaModel

    mahasiswa_db = db_session.query(MahasiswaModel).filter_by(nim="2025000005").first()
    assert mahasiswa_db is not None
    assert mahasiswa_db.nama == "Eve Polastri"


def test_create_mahasiswa_duplicate_nim(client: TestClient, setup_mahasiswa_data):
    """
    Test creating a Mahasiswa with an existing NIM should fail.
    """
    existing_mahasiswa, _, _, _ = setup_mahasiswa_data
    duplicate_data = {
        "nim": existing_mahasiswa.nim,  # NIM sudah ada
        "nama": "Fake Duplicate",
        "kelas": "TI-2A",
        "tempat_lahir": "Denpasar",
        "tanggal_lahir": "2000-05-05",
    }

    response = client.post("/mahasiswa/", json=duplicate_data)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]


def test_create_mahasiswa_missing_fields(client: TestClient):
    """
    Test creating Mahasiswa with missing required fields.
    """
    invalid_data = {
        "nim": "2025000006",
        # "nama" missing
        "kelas": "TI-2A",
        "tempat_lahir": "Surabaya",
        "tanggal_lahir": "2000-10-10",
    }

    response = client.post("/mahasiswa/", json=invalid_data)
    assert response.status_code == 422  # validation error (FastAPI default)


def test_create_mahasiswa_invalid_date_format(client: TestClient):
    """
    Test creating Mahasiswa with invalid date format.
    """
    invalid_data = {
        "nim": "2025000007",
        "nama": "Invalid Date",
        "kelas": "TI-3F",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "2000/12/31",  # invalid format
    }

    response = client.post("/mahasiswa/", json=invalid_data)
    assert response.status_code == 422


def test_create_mahasiswa_future_date(client: TestClient):
    """
    Test creating Mahasiswa with a future birth date.
    """
    future_date = (date.today() + timedelta(days=30)).isoformat()
    invalid_data = {
        "nim": "2025000008",
        "nama": "Time Traveler",
        "kelas": "TI-3G",
        "tempat_lahir": "Mars",
        "tanggal_lahir": future_date,
    }

    response = client.post("/mahasiswa/", json=invalid_data)
    assert response.status_code == 201

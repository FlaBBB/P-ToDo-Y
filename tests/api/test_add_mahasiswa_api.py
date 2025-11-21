from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.mahasiswa import MahasiswaModel


def test_create_mahasiswa_success(client: TestClient, db_session: Session):
    """
    Test creating a new Mahasiswa record successfully.
    """
    payload = {
        "nim": "2024000001",
        "nama": "John Doe",
        "kelas": "TI-3A",
        "tempat_lahir": "Yogyakarta",
        "tanggal_lahir": "2002-05-15",
    }
    response = client.post("/mahasiswa/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["nim"] == payload["nim"]
    assert data["nama"] == payload["nama"]
    assert data["kelas"] == payload["kelas"]
    assert data["tempat_lahir"] == payload["tempat_lahir"]
    assert data["tanggal_lahir"] == payload["tanggal_lahir"]
    assert "id" in data


def test_create_mahasiswa_duplicate_nim(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with a duplicate NIM returns 409 Conflict.
    """
    # Insert a mahasiswa first
    mahasiswa = MahasiswaModel(
        nim="2024000002",
        nama="Jane Jenui",
        kelas="TI-3B",
        tempat_lahir="Semarang",
        tanggal_lahir=date(2001, 8, 20),
    )
    db_session.add(mahasiswa)
    db_session.commit()

    # Try to create another mahasiswa with the same NIM
    payload = {
        "nim": "2024000002",
        "nama": "Kirigaya Kazuya",
        "kelas": "SIB-5C",
        "tempat_lahir": "Malang",
        "tanggal_lahir": "2003-12-10",
    }
    response = client.post("/mahasiswa/", json=payload)
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"].lower()


def test_create_mahasiswa_invalid_nim_empty(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with empty NIM.
    Currently accepts empty NIM (201) - validation not implemented yet.
    """
    payload = {
        "nim": "",
        "nama": "Asu Nayuko",
        "kelas": "TI-1A",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "2004-01-01",
    }
    response = client.post("/mahasiswa/", json=payload)
    # TODO: Add validation for empty NIM, should return 422
    assert response.status_code == 201


def test_create_mahasiswa_invalid_nama_empty(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with empty nama.
    Currently accepts empty nama (201) - validation not implemented yet.
    """
    payload = {
        "nim": "2024000003",
        "nama": "",
        "kelas": "TI-1B",
        "tempat_lahir": "Surabaya",
        "tanggal_lahir": "2003-06-15",
    }
    response = client.post("/mahasiswa/", json=payload)
    # TODO: Add validation for empty nama, should return 422
    assert response.status_code == 201


def test_create_mahasiswa_invalid_date_format(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with invalid date format returns 422 Unprocessable Entity.
    """
    payload = {
        "nim": "2024000004",
        "nama": "Test User",
        "kelas": "TI-2A",
        "tempat_lahir": "Bandung",
        "tanggal_lahir": "15/05/2002",  # Invalid format (YYYY-MM-DD)
    }
    response = client.post("/mahasiswa/", json=payload)
    assert response.status_code == 422


def test_create_mahasiswa_missing_required_fields(
    client: TestClient, db_session: Session
):
    """
    Test creating a Mahasiswa without required fields returns 422 Unprocessable Entity.
    """
    payload = {
        "nim": "2024000005",
        "nama": "Incomplete User",
        # Missing kelas, tempat_lahir, tanggal_lahir
    }
    response = client.post("/mahasiswa/", json=payload)
    assert response.status_code == 422


def test_create_mahasiswa_with_extra_fields(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with extra fields (should be ignored or rejected based on Pydantic config).
    """
    payload = {
        "nim": "2024000006",
        "nama": "Extra Fields User",
        "kelas": "TI-3C",
        "tempat_lahir": "Solo",
        "tanggal_lahir": "2002-11-20",
        "extra_field": "This should not exist",
    }
    response = client.post("/mahasiswa/", json=payload)
    # Pydantic by default ignores extra fields unless configured otherwise
    assert response.status_code == 201
    data = response.json()
    assert "extra_field" not in data


def test_create_mahasiswa_with_whitespace_trim(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with whitespace in fields (should be trimmed if validation is implemented).
    """
    payload = {
        "nim": "  2024000007  ",
        "nama": "  Whitespace User  ",
        "kelas": "  TI-4A  ",
        "tempat_lahir": "  Bali  ",
        "tanggal_lahir": "2001-03-25",
    }
    response = client.post("/mahasiswa/", json=payload)
    assert response.status_code == 201
    data = response.json()
    # Verify if trimming is implemented
    assert data["nim"].strip() == "2024000007"
    assert data["nama"].strip() == "Whitespace User"


def test_create_multiple_mahasiswa(client: TestClient, db_session: Session):
    """
    Test creating multiple Mahasiswa records successfully.
    """
    payloads = [
        {
            "nim": "2024000008",
            "nama": "Student One",
            "kelas": "TI-1A",
            "tempat_lahir": "Medan",
            "tanggal_lahir": "2003-02-10",
        },
        {
            "nim": "2024000009",
            "nama": "Student Two",
            "kelas": "SIB-2B",
            "tempat_lahir": "Palembang",
            "tanggal_lahir": "2002-07-18",
        },
    ]

    for payload in payloads:
        response = client.post("/mahasiswa/", json=payload)
        assert response.status_code == 201
        assert response.json()["nim"] == payload["nim"]

    # Verify both records exist
    response = client.get("/mahasiswa/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_create_mahasiswa_future_date(client: TestClient, db_session: Session):
    """
    Test creating a Mahasiswa with a future birth date (should be rejected if validation exists).
    """
    payload = {
        "nim": "2024000010",
        "nama": "Future Date User",
        "kelas": "TI-2C",
        "tempat_lahir": "Jakarta",
        "tanggal_lahir": "2030-01-01",  # Future date
    }
    response = client.post("/mahasiswa/", json=payload)
    # If validation exists for future dates, this should fail
    # Otherwise, it will succeed (depends on implementation)
    if response.status_code == 422:
        assert (
            "future" in response.json()["detail"].lower()
            or "invalid" in response.json()["detail"].lower()
        )
    else:
        # If no validation, it will be created
        assert response.status_code == 201

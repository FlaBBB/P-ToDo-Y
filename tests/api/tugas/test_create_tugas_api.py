from datetime import date, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.mahasiswa import MahasiswaModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel
from src.repositories.database.models.tugas import TugasModel


def test_create_tugas_success(client: TestClient, db_session: Session):
    """
    Test creating a new Tugas record successfully.
    """
    # Setup mata kuliah
    mata_kuliah = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman Dasar", sks=3)
    db_session.add(mata_kuliah)
    db_session.commit()
    db_session.refresh(mata_kuliah)

    # Setup mahasiswa
    mahasiswa = MahasiswaModel(
        nim="2024001",
        nama="John Doe",
        kelas="A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2005, 1, 1),
    )
    db_session.add(mahasiswa)
    db_session.commit()
    db_session.refresh(mahasiswa)

    payload = {
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi web dengan FastAPI",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mata_kuliah_id": mata_kuliah.id,
        "mahasiswa_id": mahasiswa.id,
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["judul"] == payload["judul"]
    assert data["deskripsi"] == payload["deskripsi"]
    assert data["status"] == payload["status"]
    assert data["mata_kuliah_id"] == mata_kuliah.id
    assert data["mahasiswa_id"] == mahasiswa.id
    assert "id" in data


def test_create_tugas_minimal(client: TestClient, db_session: Session):
    """
    Test creating a Tugas with minimal required fields.
    """
    payload = {
        "judul": "Tugas Mingguan",
        "deskripsi": "Latihan soal matematika",
        "deadline": "2025-12-31T23:59:59",
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["judul"] == payload["judul"]
    assert data["deskripsi"] == payload["deskripsi"]
    assert data["status"] == "pending"  # Default status
    assert data["mata_kuliah_id"] is None
    assert data["mahasiswa_id"] is None
    assert "id" in data


def test_create_tugas_with_valid_mata_kuliah(client: TestClient, db_session: Session):
    """
    Test creating a Tugas with valid mata_kuliah_id.
    """
    # Setup mata kuliah
    mata_kuliah = MataKuliahModel(kode_mk="IF201", nama_mk="Struktur Data", sks=4)
    db_session.add(mata_kuliah)
    db_session.commit()
    db_session.refresh(mata_kuliah)

    payload = {
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi web",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mata_kuliah_id": mata_kuliah.id,
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["mata_kuliah_id"] == mata_kuliah.id


def test_create_tugas_with_valid_mahasiswa(client: TestClient, db_session: Session):
    """
    Test creating a Tugas with valid mahasiswa_id.
    """
    # Setup mahasiswa
    mahasiswa = MahasiswaModel(
        nim="2024999",
        nama="Jane Doe",
        kelas="B",
        tempat_lahir="Bandung",
        tanggal_lahir=date(2005, 3, 15),
    )
    db_session.add(mahasiswa)
    db_session.commit()
    db_session.refresh(mahasiswa)

    payload = {
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi web",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mahasiswa_id": mahasiswa.id,
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["mahasiswa_id"] == mahasiswa.id


def test_create_tugas_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test creating a Tugas without required fields returns 422.
    """
    payload = {
        "judul": "Tugas UAS",
        # Missing deskripsi and deadline
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 422


def test_create_tugas_invalid_status(client: TestClient, db_session: Session):
    """
    Test creating a Tugas with invalid status returns 422.
    """
    payload = {
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi web",
        "deadline": "2025-12-31T23:59:59",
        "status": "invalid_status",  # Invalid status
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 422


def test_create_tugas_invalid_deadline_format(client: TestClient, db_session: Session):
    """
    Test creating a Tugas with invalid deadline format returns 422.
    """
    payload = {
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi web",
        "deadline": "31-12-2025",  # Invalid format
        "status": "pending",
    }
    response = client.post("/tugas/", json=payload)
    assert response.status_code == 422


def test_create_tugas_with_all_status_types(
    client: TestClient, db_session: Session
):
    """
    Test creating Tugas with different status types.
    """
    statuses = ["pending", "in_progress", "done", "cancelled"]

    for status in statuses:
        payload = {
            "judul": f"Tugas {status}",
            "deskripsi": "Test tugas",
            "deadline": "2025-12-31T23:59:59",
            "status": status,
        }
        response = client.post("/tugas/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == status

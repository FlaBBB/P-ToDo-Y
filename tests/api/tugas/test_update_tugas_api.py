from datetime import date, datetime
import warnings

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Suppress Pydantic deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")

from src.repositories.database.models.mahasiswa import MahasiswaModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel
from src.repositories.database.models.tugas import TugasModel


def test_update_tugas_success(client: TestClient, db_session: Session):
    """
    Test updating a Tugas successfully.
    """
    tugas = TugasModel(
        judul="Tugas Lama",
        deskripsi="Deskripsi lama",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas Baru",
        "deskripsi": "Deskripsi baru",
        "deadline": "2025-12-30T23:59:59",
        "status": "in_progress",
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tugas.id
    assert data["judul"] == "Tugas Baru"
    assert data["deskripsi"] == "Deskripsi baru"
    assert data["status"] == "in_progress"


def test_update_tugas_not_found(client: TestClient, db_session: Session):
    """
    Test updating a non-existent Tugas returns 404 Not Found.
    """
    payload = {
        "id": 999,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
    }
    response = client.put("/tugas/999", json=payload)
    assert response.status_code == 404


def test_update_tugas_change_status(client: TestClient, db_session: Session):
    """
    Test updating Tugas status from pending to done.
    """
    tugas = TugasModel(
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas UAS",
        "deskripsi": "Membuat aplikasi",
        "deadline": "2025-12-31T23:59:59",
        "status": "done",
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"


def test_update_tugas_add_mata_kuliah(client: TestClient, db_session: Session):
    """
    Test adding mata_kuliah_id to an existing Tugas.
    """
    # Setup mata kuliah
    mk = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    db_session.add(mk)
    db_session.commit()
    db_session.refresh(mk)

    # Setup tugas without mata_kuliah
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mata_kuliah_id": mk.id,
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mata_kuliah_id"] == mk.id


def test_update_tugas_add_mahasiswa(client: TestClient, db_session: Session):
    """
    Test adding mahasiswa_id to an existing Tugas.
    """
    # Setup mahasiswa
    mhs = MahasiswaModel(
        nim="2024001",
        nama="John Doe",
        kelas="A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2005, 1, 1),
    )
    db_session.add(mhs)
    db_session.commit()
    db_session.refresh(mhs)

    # Setup tugas without mahasiswa
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mahasiswa_id": mhs.id,
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mahasiswa_id"] == mhs.id


def test_update_tugas_change_mata_kuliah(client: TestClient, db_session: Session):
    """
    Test changing mata_kuliah_id of an existing Tugas.
    """
    # Setup mata kuliah
    mk1 = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    mk2 = MataKuliahModel(kode_mk="IF102", nama_mk="Database", sks=3)
    db_session.add_all([mk1, mk2])
    db_session.commit()
    db_session.refresh(mk1)
    db_session.refresh(mk2)

    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk1.id,
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mata_kuliah_id": mk2.id,  # Change to mk2
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mata_kuliah_id"] == mk2.id


def test_update_tugas_change_mahasiswa(client: TestClient, db_session: Session):
    """
    Test changing mahasiswa_id of an existing Tugas.
    """
    # Setup mahasiswa
    mhs1 = MahasiswaModel(
        nim="2024001",
        nama="John Doe",
        kelas="A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2005, 1, 1),
    )
    mhs2 = MahasiswaModel(
        nim="2024002",
        nama="Jane Smith",
        kelas="A",
        tempat_lahir="Bandung",
        tanggal_lahir=date(2005, 2, 1),
    )
    db_session.add_all([mhs1, mhs2])
    db_session.commit()
    db_session.refresh(mhs1)
    db_session.refresh(mhs2)

    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mahasiswa_id=mhs1.id,
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "pending",
        "mahasiswa_id": mhs2.id,  # Change to mhs2
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mahasiswa_id"] == mhs2.id


def test_update_tugas_invalid_status(client: TestClient, db_session: Session):
    """
    Test updating Tugas with invalid status returns 422.
    """
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": "2025-12-31T23:59:59",
        "status": "invalid_status",  # Invalid
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 422


def test_update_tugas_change_deadline(client: TestClient, db_session: Session):
    """
    Test updating Tugas deadline.
    """
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    new_deadline = "2026-01-15T23:59:59"
    payload = {
        "id": tugas.id,
        "judul": "Tugas",
        "deskripsi": "Deskripsi",
        "deadline": new_deadline,
        "status": "pending",
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert new_deadline in data["deadline"]


def test_update_tugas_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test updating Tugas without required fields returns 422.
    """
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    payload = {
        "id": tugas.id,
        "judul": "Tugas Updated",
        # Missing other required fields
    }
    response = client.put(f"/tugas/{tugas.id}", json=payload)
    assert response.status_code == 422


def test_update_tugas_all_status_transitions(client: TestClient, db_session: Session):
    """
    Test transitioning through all status states.
    """
    tugas = TugasModel(
        judul="Tugas",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    statuses = ["pending", "in_progress", "done", "cancelled"]

    for status in statuses:
        payload = {
            "id": tugas.id,
            "judul": "Tugas",
            "deskripsi": "Deskripsi",
            "deadline": "2025-12-31T23:59:59",
            "status": status,
        }
        response = client.put(f"/tugas/{tugas.id}", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == status

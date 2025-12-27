from datetime import date, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.mahasiswa import MahasiswaModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel
from src.repositories.database.models.tugas import TugasModel


def setup_tugas_for_delete(db_session: Session):
    """
    Setup Tugas data for DELETE tests.
    """
    # Create Mata Kuliah
    mk = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman Dasar", sks=3)

    # Create Mahasiswa
    mhs = MahasiswaModel(
        nim="2024001",
        nama="John Doe",
        kelas="A",
        tempat_lahir="Jakarta",
        tanggal_lahir=date(2005, 1, 1),
    )

    db_session.add_all([mk, mhs])
    db_session.commit()
    db_session.refresh(mk)
    db_session.refresh(mhs)

    # Create Tugas
    tugas1 = TugasModel(
        judul="Tugas 1",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk.id,
        mahasiswa_id=mhs.id,
    )
    tugas2 = TugasModel(
        judul="Tugas 2",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="in_progress",
        mata_kuliah_id=mk.id,
        mahasiswa_id=mhs.id,
    )
    tugas3 = TugasModel(
        judul="Tugas 3",
        deskripsi="Deskripsi 3",
        deadline=datetime(2025, 12, 29, 23, 59, 59),
        status="done",
    )

    db_session.add_all([tugas1, tugas2, tugas3])
    db_session.commit()
    db_session.refresh(tugas1)
    db_session.refresh(tugas2)
    db_session.refresh(tugas3)

    return tugas1, tugas2, tugas3


def test_delete_tugas_success(client: TestClient, db_session: Session):
    """
    Test deleting a Tugas successfully (soft delete - changes status to CANCELLED).
    """
    tugas1, tugas2, tugas3 = setup_tugas_for_delete(db_session)

    response = client.delete(f"/tugas/{tugas1.id}")
    assert response.status_code == 204

    # Verify the tugas status was changed to CANCELLED (soft delete)
    response_get = client.get(f"/tugas/?id={tugas1.id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert len(data) == 1
    assert data[0]["status"] == "cancelled"

    # Verify other tugas still exist
    response_all = client.get("/tugas/")
    assert response_all.status_code == 200
    data_all = response_all.json()
    assert len(data_all) == 3  # All 3 still exist, one is cancelled


def test_delete_tugas_not_found(client: TestClient, db_session: Session):
    """
    Test deleting a non-existent Tugas returns 404 Not Found.
    """
    response = client.delete("/tugas/999")
    assert response.status_code == 404


def test_delete_tugas_by_id_multiple_times(client: TestClient, db_session: Session):
    """
    Test that only delete by ID is supported (not bulk delete by query params).
    """
    tugas1 = TugasModel(
        judul="Tugas 1",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    tugas2 = TugasModel(
        judul="Tugas 2",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="pending",
    )
    db_session.add_all([tugas1, tugas2])
    db_session.commit()
    db_session.refresh(tugas1)
    db_session.refresh(tugas2)

    # Delete first tugas
    response1 = client.delete(f"/tugas/{tugas1.id}")
    assert response1.status_code == 204

    # Delete second tugas
    response2 = client.delete(f"/tugas/{tugas2.id}")
    assert response2.status_code == 204

    # Verify both are cancelled
    response_all = client.get("/tugas/")
    assert response_all.status_code == 200
    data_all = response_all.json()
    assert len(data_all) == 2
    assert all(t["status"] == "cancelled" for t in data_all)


def test_delete_tugas_with_different_statuses(client: TestClient, db_session: Session):
    """
    Test deleting tugas with different initial statuses.
    """
    tugas1 = TugasModel(
        judul="Tugas Pending",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    tugas2 = TugasModel(
        judul="Tugas In Progress",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="in_progress",
    )
    tugas3 = TugasModel(
        judul="Tugas Done",
        deskripsi="Deskripsi 3",
        deadline=datetime(2025, 12, 29, 23, 59, 59),
        status="done",
    )
    db_session.add_all([tugas1, tugas2, tugas3])
    db_session.commit()
    db_session.refresh(tugas1)
    db_session.refresh(tugas2)
    db_session.refresh(tugas3)

    # Delete all tugas
    response1 = client.delete(f"/tugas/{tugas1.id}")
    assert response1.status_code == 204

    response2 = client.delete(f"/tugas/{tugas2.id}")
    assert response2.status_code == 204

    response3 = client.delete(f"/tugas/{tugas3.id}")
    assert response3.status_code == 204

    # Verify all are cancelled
    response_all = client.get("/tugas/")
    assert response_all.status_code == 200
    data_all = response_all.json()
    assert len(data_all) == 3
    assert all(t["status"] == "cancelled" for t in data_all)


def test_delete_tugas_with_mata_kuliah(client: TestClient, db_session: Session):
    """
    Test deleting a Tugas that has mata_kuliah_id.
    """
    # Setup mata kuliah
    mk = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    db_session.add(mk)
    db_session.commit()
    db_session.refresh(mk)

    # Setup tugas
    tugas = TugasModel(
        judul="Tugas Pemrograman",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk.id,
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    response = client.delete(f"/tugas/{tugas.id}")
    assert response.status_code == 204

    # Verify the tugas is cancelled
    response_get = client.get(f"/tugas/?id={tugas.id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert len(data) == 1
    assert data[0]["status"] == "cancelled"
    assert data[0]["mata_kuliah_id"] == mk.id  # Relations still intact


def test_delete_tugas_with_mahasiswa(client: TestClient, db_session: Session):
    """
    Test deleting a Tugas that has mahasiswa_id.
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

    # Setup tugas
    tugas = TugasModel(
        judul="Tugas John",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mahasiswa_id=mhs.id,
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    response = client.delete(f"/tugas/{tugas.id}")
    assert response.status_code == 204

    # Verify the tugas is cancelled
    response_get = client.get(f"/tugas/?id={tugas.id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert len(data) == 1
    assert data[0]["status"] == "cancelled"
    assert data[0]["mahasiswa_id"] == mhs.id  # Relations still intact


def test_delete_multiple_tugas(client: TestClient, db_session: Session):
    """
    Test deleting multiple tugas one by one.
    """
    tugas1, tugas2, tugas3 = setup_tugas_for_delete(db_session)

    # Delete first tugas
    response1 = client.delete(f"/tugas/{tugas1.id}")
    assert response1.status_code == 204

    # Delete second tugas
    response2 = client.delete(f"/tugas/{tugas2.id}")
    assert response2.status_code == 204

    # Verify all three still exist but two are cancelled
    response_all = client.get("/tugas/")
    assert response_all.status_code == 200
    data_all = response_all.json()
    assert len(data_all) == 3
    cancelled_count = sum(1 for t in data_all if t["status"] == "cancelled")
    assert cancelled_count == 2


def test_delete_tugas_twice(client: TestClient, db_session: Session):
    """
    Test deleting the same Tugas twice (soft delete is idempotent).
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

    # First delete should succeed
    response1 = client.delete(f"/tugas/{tugas.id}")
    assert response1.status_code == 204

    # Second delete should also succeed (idempotent)
    response2 = client.delete(f"/tugas/{tugas.id}")
    assert response2.status_code == 204

    # Verify still cancelled
    response_get = client.get(f"/tugas/?id={tugas.id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert len(data) == 1
    assert data[0]["status"] == "cancelled"


def test_delete_tugas_with_all_relations(client: TestClient, db_session: Session):
    """
    Test deleting a Tugas that has both mata_kuliah_id and mahasiswa_id.
    """
    # Setup mata kuliah
    mk = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    db_session.add(mk)
    db_session.commit()
    db_session.refresh(mk)

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

    # Setup tugas with both relations
    tugas = TugasModel(
        judul="Tugas Kompleks",
        deskripsi="Deskripsi",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk.id,
        mahasiswa_id=mhs.id,
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    response = client.delete(f"/tugas/{tugas.id}")
    assert response.status_code == 204

    # Verify the tugas is cancelled with relations intact
    response_get = client.get(f"/tugas/?id={tugas.id}")
    assert response_get.status_code == 200
    data = response_get.json()
    assert len(data) == 1
    assert data[0]["status"] == "cancelled"
    assert data[0]["mata_kuliah_id"] == mk.id
    assert data[0]["mahasiswa_id"] == mhs.id
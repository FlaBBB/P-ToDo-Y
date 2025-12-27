from datetime import date, datetime

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.mahasiswa import MahasiswaModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel
from src.repositories.database.models.tugas import TugasModel


def test_get_all_tugas(client: TestClient, db_session: Session):
    """
    Test getting all Tugas records.
    """
    # Setup data
    tugas1 = TugasModel(
        judul="Tugas 1",
        deskripsi="Deskripsi tugas 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    tugas2 = TugasModel(
        judul="Tugas 2",
        deskripsi="Deskripsi tugas 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="in_progress",
    )
    db_session.add_all([tugas1, tugas2])
    db_session.commit()

    response = client.get("/tugas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["judul"] == "Tugas 1"
    assert data[1]["judul"] == "Tugas 2"


def test_get_tugas_by_id(client: TestClient, db_session: Session):
    """
    Test getting a Tugas by ID.
    """
    tugas = TugasModel(
        judul="Tugas UAS",
        deskripsi="Membuat aplikasi web",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    db_session.add(tugas)
    db_session.commit()
    db_session.refresh(tugas)

    response = client.get(f"/tugas/?id={tugas.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == tugas.id
    assert data[0]["judul"] == "Tugas UAS"
    assert data[0]["status"] == "pending"


def test_get_tugas_by_judul(client: TestClient, db_session: Session):
    """
    Test getting Tugas by judul.
    """
    tugas1 = TugasModel(
        judul="Tugas Pemrograman",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
    )
    tugas2 = TugasModel(
        judul="Tugas Matematika",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="pending",
    )
    db_session.add_all([tugas1, tugas2])
    db_session.commit()

    response = client.get("/tugas/?judul=Pemrograman")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["judul"] == "Tugas Pemrograman"


def test_get_tugas_by_status(client: TestClient, db_session: Session):
    """
    Test getting Tugas by status.
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
        status="done",
    )
    tugas3 = TugasModel(
        judul="Tugas 3",
        deskripsi="Deskripsi 3",
        deadline=datetime(2025, 12, 29, 23, 59, 59),
        status="pending",
    )
    db_session.add_all([tugas1, tugas2, tugas3])
    db_session.commit()

    response = client.get("/tugas/?status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["status"] == "pending" for t in data)


def test_get_tugas_by_mata_kuliah_id(client: TestClient, db_session: Session):
    """
    Test getting Tugas by mata_kuliah_id.
    """
    # Setup mata kuliah
    mk1 = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    mk2 = MataKuliahModel(kode_mk="IF102", nama_mk="Database", sks=3)
    db_session.add_all([mk1, mk2])
    db_session.commit()
    db_session.refresh(mk1)
    db_session.refresh(mk2)

    # Setup tugas
    tugas1 = TugasModel(
        judul="Tugas Pemrograman",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk1.id,
    )
    tugas2 = TugasModel(
        judul="Tugas Database",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk2.id,
    )
    db_session.add_all([tugas1, tugas2])
    db_session.commit()

    response = client.get(f"/tugas/?mata_kuliah_id={mk1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["mata_kuliah_id"] == mk1.id


def test_get_tugas_by_mahasiswa_id(client: TestClient, db_session: Session):
    """
    Test getting Tugas by mahasiswa_id.
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

    # Setup tugas
    tugas1 = TugasModel(
        judul="Tugas John",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mahasiswa_id=mhs1.id,
    )
    tugas2 = TugasModel(
        judul="Tugas Jane",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="pending",
        mahasiswa_id=mhs2.id,
    )
    db_session.add_all([tugas1, tugas2])
    db_session.commit()

    response = client.get(f"/tugas/?mahasiswa_id={mhs1.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["mahasiswa_id"] == mhs1.id


def test_get_tugas_not_found(client: TestClient, db_session: Session):
    """
    Test getting a non-existent Tugas returns empty list.
    """
    response = client.get("/tugas/?id=999")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_tugas_empty_database(client: TestClient, db_session: Session):
    """
    Test getting all Tugas from empty database returns empty list.
    """
    response = client.get("/tugas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_tugas_multiple_filters(client: TestClient, db_session: Session):
    """
    Test getting Tugas with multiple filters (status and mata_kuliah_id).
    """
    # Setup mata kuliah
    mk = MataKuliahModel(kode_mk="IF101", nama_mk="Pemrograman", sks=3)
    db_session.add(mk)
    db_session.commit()
    db_session.refresh(mk)

    # Setup tugas
    tugas1 = TugasModel(
        judul="Tugas 1",
        deskripsi="Deskripsi 1",
        deadline=datetime(2025, 12, 31, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk.id,
    )
    tugas2 = TugasModel(
        judul="Tugas 2",
        deskripsi="Deskripsi 2",
        deadline=datetime(2025, 12, 30, 23, 59, 59),
        status="done",
        mata_kuliah_id=mk.id,
    )
    tugas3 = TugasModel(
        judul="Tugas 3",
        deskripsi="Deskripsi 3",
        deadline=datetime(2025, 12, 29, 23, 59, 59),
        status="pending",
        mata_kuliah_id=mk.id,
    )
    db_session.add_all([tugas1, tugas2, tugas3])
    db_session.commit()

    response = client.get(f"/tugas/?mata_kuliah_id={mk.id}&status=pending")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(t["status"] == "pending" for t in data)
    assert all(t["mata_kuliah_id"] == mk.id for t in data)

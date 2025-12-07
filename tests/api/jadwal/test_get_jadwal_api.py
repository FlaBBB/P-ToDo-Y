import pytest
from datetime import time

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel
from src.repositories.database.models.jadwal import JadwalModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


def setup_jadwal_data(db_session: Session):
    """
    Setup Jadwal data with dependencies for GET tests.
    """
    # Create Dosen
    dosen1 = DosenModel(nidn="1111111111", nama="Dr. Alice", email="alice@example.com")
    dosen2 = DosenModel(nidn="2222222222", nama="Dr. Bob", email="bob@example.com")

    # Create Mata Kuliah
    mk1 = MataKuliahModel(kode_mk="IF201", nama_mk="Struktur Data", sks=3)
    mk2 = MataKuliahModel(kode_mk="IF202", nama_mk="Basis Data", sks=4)

    db_session.add_all([dosen1, dosen2, mk1, mk2])
    db_session.commit()
    db_session.refresh(dosen1)
    db_session.refresh(dosen2)
    db_session.refresh(mk1)
    db_session.refresh(mk2)

    # Create Jadwal
    jadwal1 = JadwalModel(
        hari="Senin",
        jam_mulai=time(8, 0, 0),
        jam_selesai=time(10, 0, 0),
        ruangan="A101",
        mata_kuliah_id=mk1.id,
        dosen_id=dosen1.id,
    )
    jadwal2 = JadwalModel(
        hari="Selasa",
        jam_mulai=time(10, 0, 0),
        jam_selesai=time(12, 0, 0),
        ruangan="B201",
        mata_kuliah_id=mk2.id,
        dosen_id=dosen2.id,
    )
    jadwal3 = JadwalModel(
        hari="Rabu",
        jam_mulai=time(13, 0, 0),
        jam_selesai=time(15, 0, 0),
        ruangan="A101",
        mata_kuliah_id=mk1.id,
        dosen_id=dosen1.id,
    )
    jadwal4 = JadwalModel(
        hari="Kamis",
        jam_mulai=time(8, 0, 0),
        jam_selesai=time(10, 0, 0),
        ruangan="C301",
        mata_kuliah_id=mk2.id,
        dosen_id=dosen1.id,
    )

    db_session.add_all([jadwal1, jadwal2, jadwal3, jadwal4])
    db_session.commit()
    db_session.refresh(jadwal1)
    db_session.refresh(jadwal2)
    db_session.refresh(jadwal3)
    db_session.refresh(jadwal4)

    return jadwal1, jadwal2, jadwal3, jadwal4


def test_get_all_jadwal(client: TestClient, db_session: Session):
    """
    Test retrieving all Jadwal records.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/")
    assert response.status_code == 200
    assert len(response.json()) == 4
    assert response.json()[0]["hari"] == "Senin"


def test_get_jadwal_by_id(client: TestClient, db_session: Session):
    """
    Test retrieving a specific Jadwal record by ID.
    """
    jadwal1, _, _, _ = setup_jadwal_data(db_session)
    response = client.get(f"/jadwal/?id={jadwal1.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["hari"] == jadwal1.hari


def test_get_jadwal_by_hari(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records by hari (day).
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?hari=Senin")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["hari"] == "Senin"


def test_get_jadwal_by_ruangan(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records by ruangan (room).
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?ruangan=A101")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert all(j["ruangan"] == "A101" for j in results)


def test_get_jadwal_by_mata_kuliah_id(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records by mata_kuliah_id.
    """
    jadwal1, _, _, _ = setup_jadwal_data(db_session)
    response = client.get(f"/jadwal/?mata_kuliah_id={jadwal1.mata_kuliah_id}")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert all(j["mata_kuliah_id"] == jadwal1.mata_kuliah_id for j in results)


def test_get_jadwal_by_dosen_id(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records by dosen_id.
    """
    jadwal1, _, _, _ = setup_jadwal_data(db_session)
    response = client.get(f"/jadwal/?dosen_id={jadwal1.dosen_id}")
    assert response.status_code == 200
    results = response.json()
    assert len(results) >= 1
    assert all(j["dosen_id"] == jadwal1.dosen_id for j in results)


def test_get_jadwal_with_pagination_limit(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records with a limit.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_jadwal_with_pagination_limit_and_page(
    client: TestClient, db_session: Session
):
    """
    Test retrieving Jadwal records with limit and page.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?limit=2&page=2&order_by=hari&order=asc")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2


def test_get_jadwal_with_ordering_asc(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records with ascending order by hari.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?order_by=hari&order=asc")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    assert results[0]["hari"] == "Kamis"  # Alphabetically first


def test_get_jadwal_with_ordering_desc(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records with descending order by hari.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?order_by=hari&order=desc")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    assert results[0]["hari"] == "Senin"  # Alphabetically last


def test_get_jadwal_not_found_by_id(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal with non-existent ID returns empty list.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?id=99999")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_jadwal_not_found_by_hari(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal with non-existent hari returns empty list.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?hari=Sabtu")
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_get_jadwal_combined_filters(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records with multiple filters combined.
    """
    jadwal1, _, _, _ = setup_jadwal_data(db_session)
    response = client.get(
        f"/jadwal/?hari=Senin&ruangan=A101&dosen_id={jadwal1.dosen_id}"
    )
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["hari"] == "Senin"
    assert results[0]["ruangan"] == "A101"


def test_get_jadwal_by_jam_mulai(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal records by jam_mulai.
    """
    setup_jadwal_data(db_session)
    response = client.get("/jadwal/?jam_mulai=08:00:00")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert all(j["jam_mulai"] == "08:00:00" for j in results)


def test_get_jadwal_empty_database(client: TestClient, db_session: Session):
    """
    Test retrieving Jadwal when database is empty returns empty list.
    """
    response = client.get("/jadwal/")
    assert response.status_code == 200
    assert len(response.json()) == 0

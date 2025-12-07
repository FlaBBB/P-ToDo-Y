from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


def setup_dependencies(db_session: Session):
    """
    Setup Dosen and Mata Kuliah as dependencies for Jadwal tests.
    """
    # Create Dosen
    dosen = DosenModel(
        nidn="1234567890",
        nama="Dr. John Doe",
        email="john.doe@example.com",
    )
    db_session.add(dosen)

    # Create Mata Kuliah
    mata_kuliah = MataKuliahModel(
        kode_mk="IF101",
        nama_mk="Pemrograman Dasar",
        sks=3,
    )
    db_session.add(mata_kuliah)
    db_session.commit()
    db_session.refresh(dosen)
    db_session.refresh(mata_kuliah)

    return dosen, mata_kuliah


def test_create_jadwal_success(client: TestClient, db_session: Session):
    """
    Test creating a new Jadwal record successfully.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "Senin",
        "jam_mulai": "08:00:00",
        "jam_selesai": "10:00:00",
        "ruangan": "A101",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["hari"] == payload["hari"]
    assert data["jam_mulai"] == payload["jam_mulai"]
    assert data["jam_selesai"] == payload["jam_selesai"]
    assert data["ruangan"] == payload["ruangan"]
    assert data["mata_kuliah_id"] == payload["mata_kuliah_id"]
    assert data["dosen_id"] == payload["dosen_id"]
    assert "id" in data


def test_create_jadwal_invalid_time_range(client: TestClient, db_session: Session):
    """
    Test creating Jadwal with jam_mulai >= jam_selesai returns 422 Unprocessable Entity.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "Selasa",
        "jam_mulai": "10:00:00",
        "jam_selesai": "08:00:00",  # Invalid: jam_selesai before jam_mulai
        "ruangan": "A102",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 422
    assert "before" in response.json()["detail"].lower()


def test_create_jadwal_same_time(client: TestClient, db_session: Session):
    """
    Test creating Jadwal with jam_mulai == jam_selesai returns 422 Unprocessable Entity.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "Rabu",
        "jam_mulai": "10:00:00",
        "jam_selesai": "10:00:00",  # Invalid: same time
        "ruangan": "A103",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 422


def test_create_jadwal_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test creating Jadwal without required fields returns 422 Unprocessable Entity.
    """
    payload = {
        "hari": "Kamis",
        "jam_mulai": "08:00:00",
        # Missing jam_selesai, ruangan, mata_kuliah_id, dosen_id
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 422


def test_create_jadwal_invalid_time_format(client: TestClient, db_session: Session):
    """
    Test creating Jadwal with invalid time format returns 422 Unprocessable Entity.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "Jumat",
        "jam_mulai": "25:00:00",  # Invalid hour
        "jam_selesai": "10:00:00",
        "ruangan": "A104",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 422


def test_create_jadwal_with_extra_fields(client: TestClient, db_session: Session):
    """
    Test creating Jadwal with extra fields (should be ignored).
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "Senin",
        "jam_mulai": "13:00:00",
        "jam_selesai": "15:00:00",
        "ruangan": "B101",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
        "extra_field": "This should be ignored",
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "extra_field" not in data


def test_create_multiple_jadwal(client: TestClient, db_session: Session):
    """
    Test creating multiple Jadwal records successfully.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payloads = [
        {
            "hari": "Selasa",
            "jam_mulai": "08:00:00",
            "jam_selesai": "10:00:00",
            "ruangan": "C101",
            "mata_kuliah_id": mata_kuliah.id,
            "dosen_id": dosen.id,
        },
        {
            "hari": "Rabu",
            "jam_mulai": "10:00:00",
            "jam_selesai": "12:00:00",
            "ruangan": "C102",
            "mata_kuliah_id": mata_kuliah.id,
            "dosen_id": dosen.id,
        },
    ]

    for payload in payloads:
        response = client.post("/jadwal/", json=payload)
        assert response.status_code == 201
        assert response.json()["hari"] == payload["hari"]

    # Verify both records exist
    response = client.get("/jadwal/")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_create_jadwal_empty_string_fields(client: TestClient, db_session: Session):
    """
    Test creating Jadwal with empty string fields returns 422 or 400.
    """
    dosen, mata_kuliah = setup_dependencies(db_session)

    payload = {
        "hari": "",  # Empty
        "jam_mulai": "08:00:00",
        "jam_selesai": "10:00:00",
        "ruangan": "D101",
        "mata_kuliah_id": mata_kuliah.id,
        "dosen_id": dosen.id,
    }
    response = client.post("/jadwal/", json=payload)
    assert response.status_code in [400, 422]

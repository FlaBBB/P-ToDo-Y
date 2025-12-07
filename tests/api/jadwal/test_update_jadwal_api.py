from datetime import time

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel
from src.repositories.database.models.jadwal import JadwalModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


def setup_jadwal_for_update(db_session: Session):
    """
    Setup Jadwal data for UPDATE tests.
    """
    # Create Dosen
    dosen1 = DosenModel(
        nidn="3333333333", nama="Dr. Charlie", email="charlie@example.com"
    )
    dosen2 = DosenModel(nidn="4444444444", nama="Dr. Diana", email="diana@example.com")

    # Create Mata Kuliah
    mk1 = MataKuliahModel(kode_mk="IF301", nama_mk="Algoritma", sks=3)
    mk2 = MataKuliahModel(kode_mk="IF302", nama_mk="Jaringan Komputer", sks=3)

    db_session.add_all([dosen1, dosen2, mk1, mk2])
    db_session.commit()
    db_session.refresh(dosen1)
    db_session.refresh(dosen2)
    db_session.refresh(mk1)
    db_session.refresh(mk2)

    # Create Jadwal
    jadwal = JadwalModel(
        hari="Senin",
        jam_mulai=time(8, 0, 0),
        jam_selesai=time(10, 0, 0),
        ruangan="E101",
        mata_kuliah_id=mk1.id,
        dosen_id=dosen1.id,
    )
    db_session.add(jadwal)
    db_session.commit()
    db_session.refresh(jadwal)

    return jadwal, dosen1, dosen2, mk1, mk2


def test_update_jadwal_success(client: TestClient, db_session: Session):
    """
    Test updating an existing Jadwal record successfully.
    """
    jadwal, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Selasa",
        "jam_mulai": "10:00:00",
        "jam_selesai": "12:00:00",
        "ruangan": "E102",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == jadwal.id
    assert data["hari"] == "Selasa"
    assert data["jam_mulai"] == "10:00:00"
    assert data["jam_selesai"] == "12:00:00"
    assert data["ruangan"] == "E102"


def test_update_jadwal_not_found(client: TestClient, db_session: Session):
    """
    Test updating a non-existent Jadwal returns 404 Not Found.
    """
    _, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Rabu",
        "jam_mulai": "13:00:00",
        "jam_selesai": "15:00:00",
        "ruangan": "E103",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put("/jadwal/99999", json=payload)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_jadwal_invalid_time_range(client: TestClient, db_session: Session):
    """
    Test updating Jadwal with invalid time range returns 422 Unprocessable Entity.
    """
    jadwal, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Kamis",
        "jam_mulai": "15:00:00",
        "jam_selesai": "13:00:00",  # Invalid: jam_selesai before jam_mulai
        "ruangan": "E104",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 422
    assert "before" in response.json()["detail"].lower()


def test_update_jadwal_change_dosen(client: TestClient, db_session: Session):
    """
    Test updating Jadwal to change dosen_id successfully.
    """
    jadwal, _, dosen2, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Jumat",
        "jam_mulai": "08:00:00",
        "jam_selesai": "10:00:00",
        "ruangan": "E105",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen2.id,  # Changed dosen
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["dosen_id"] == dosen2.id


def test_update_jadwal_change_mata_kuliah(client: TestClient, db_session: Session):
    """
    Test updating Jadwal to change mata_kuliah_id successfully.
    """
    jadwal, dosen1, _, _, mk2 = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Sabtu",
        "jam_mulai": "10:00:00",
        "jam_selesai": "12:00:00",
        "ruangan": "E106",
        "mata_kuliah_id": mk2.id,  # Changed mata kuliah
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["mata_kuliah_id"] == mk2.id


def test_update_jadwal_missing_required_fields(client: TestClient, db_session: Session):
    """
    Test updating Jadwal without required fields returns 422 Unprocessable Entity.
    """
    jadwal, _, _, _, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Minggu",
        # Missing other required fields
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 422


# NOTE: FK constraints not enforced in SQLite by default
# def test_update_jadwal_invalid_mata_kuliah_id(client: TestClient, db_session: Session):
#     jadwal, dosen1, _, _, _ = setup_jadwal_for_update(db_session)
#     payload = {
#         "hari": "Senin", "jam_mulai": "08:00:00", "jam_selesai": "10:00:00",
#         "ruangan": "E107", "mata_kuliah_id": 99999, "dosen_id": dosen1.id,
#     }
#     response = client.put(f"/jadwal/{jadwal.id}", json=payload)
#     assert response.status_code in [400, 500]


def test_update_jadwal_invalid_time_format(client: TestClient, db_session: Session):
    """
    Test updating Jadwal with invalid time format returns 422 Unprocessable Entity.
    """
    jadwal, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Rabu",
        "jam_mulai": "25:00:00",  # Invalid hour
        "jam_selesai": "10:00:00",
        "ruangan": "E109",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 422


def test_update_jadwal_partial_update_not_allowed(
    client: TestClient, db_session: Session
):
    """
    Test that partial updates require all fields (PUT semantics).
    """
    jadwal, _, _, _, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Kamis",
        # Missing all other fields
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 422


def test_update_jadwal_same_time(client: TestClient, db_session: Session):
    """
    Test updating Jadwal with jam_mulai == jam_selesai returns 422 Unprocessable Entity.
    """
    jadwal, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    payload = {
        "hari": "Jumat",
        "jam_mulai": "10:00:00",
        "jam_selesai": "10:00:00",  # Same time
        "ruangan": "E110",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 422


def test_update_jadwal_verify_changes_persisted(
    client: TestClient, db_session: Session
):
    """
    Test that Jadwal updates are persisted in the database.
    """
    jadwal, dosen1, _, mk1, _ = setup_jadwal_for_update(db_session)

    # Update jadwal
    payload = {
        "hari": "Sabtu",
        "jam_mulai": "14:00:00",
        "jam_selesai": "16:00:00",
        "ruangan": "E111",
        "mata_kuliah_id": mk1.id,
        "dosen_id": dosen1.id,
    }
    response = client.put(f"/jadwal/{jadwal.id}", json=payload)
    assert response.status_code == 200

    # Verify changes
    verify_response = client.get(f"/jadwal/?id={jadwal.id}")
    assert verify_response.status_code == 200
    data = verify_response.json()[0]
    assert data["hari"] == "Sabtu"
    assert data["jam_mulai"] == "14:00:00"
    assert data["ruangan"] == "E111"

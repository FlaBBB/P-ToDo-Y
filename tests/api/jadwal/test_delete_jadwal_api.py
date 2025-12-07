from datetime import time

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel
from src.repositories.database.models.jadwal import JadwalModel
from src.repositories.database.models.mata_kuliah import MataKuliahModel


def setup_jadwal_for_delete(db_session: Session):
    """
    Setup Jadwal data for DELETE tests.
    """
    # Create Dosen
    dosen = DosenModel(nidn="5555555555", nama="Dr. Edward", email="edward@example.com")

    # Create Mata Kuliah
    mk = MataKuliahModel(kode_mk="IF401", nama_mk="Database Systems", sks=4)

    db_session.add_all([dosen, mk])
    db_session.commit()
    db_session.refresh(dosen)
    db_session.refresh(mk)

    # Create Jadwal
    jadwal1 = JadwalModel(
        hari="Senin",
        jam_mulai=time(8, 0, 0),
        jam_selesai=time(10, 0, 0),
        ruangan="F101",
        mata_kuliah_id=mk.id,
        dosen_id=dosen.id,
    )
    jadwal2 = JadwalModel(
        hari="Selasa",
        jam_mulai=time(10, 0, 0),
        jam_selesai=time(12, 0, 0),
        ruangan="F102",
        mata_kuliah_id=mk.id,
        dosen_id=dosen.id,
    )
    jadwal3 = JadwalModel(
        hari="Rabu",
        jam_mulai=time(13, 0, 0),
        jam_selesai=time(15, 0, 0),
        ruangan="F103",
        mata_kuliah_id=mk.id,
        dosen_id=dosen.id,
    )

    db_session.add_all([jadwal1, jadwal2, jadwal3])
    db_session.commit()
    db_session.refresh(jadwal1)
    db_session.refresh(jadwal2)
    db_session.refresh(jadwal3)

    return jadwal1, jadwal2, jadwal3, dosen, mk


def test_delete_jadwal_success(client: TestClient, db_session: Session):
    """
    Test deleting an existing Jadwal record returns 204 No Content.
    """
    jadwal1, _, _, _, _ = setup_jadwal_for_delete(db_session)

    response = client.delete(f"/jadwal/{jadwal1.id}")
    assert response.status_code == 204

    # Verify deletion
    verify_response = client.get(f"/jadwal/?id={jadwal1.id}")
    assert verify_response.status_code == 200
    assert len(verify_response.json()) == 0


def test_delete_jadwal_not_found(client: TestClient, db_session: Session):
    """
    Test deleting a non-existent Jadwal returns 404 Not Found.
    """
    setup_jadwal_for_delete(db_session)

    response = client.delete("/jadwal/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_jadwal_invalid_id_format(client: TestClient, db_session: Session):
    """
    Test deleting Jadwal with invalid ID format returns 422 Unprocessable Entity.
    """
    setup_jadwal_for_delete(db_session)

    response = client.delete("/jadwal/invalid_id")
    assert response.status_code == 422


def test_delete_jadwal_preserves_other_records(client: TestClient, db_session: Session):
    """
    Test that deleting a Jadwal does not affect other Jadwal records.
    """
    jadwal1, jadwal2, jadwal3, _, _ = setup_jadwal_for_delete(db_session)

    # Delete first jadwal
    delete_response = client.delete(f"/jadwal/{jadwal1.id}")
    assert delete_response.status_code == 204

    # Verify other jadwal still exist
    verify_response = client.get("/jadwal/")
    assert verify_response.status_code == 200
    data = verify_response.json()
    assert len(data) == 2
    remaining_ids = [item["id"] for item in data]
    assert jadwal2.id in remaining_ids
    assert jadwal3.id in remaining_ids
    assert jadwal1.id not in remaining_ids


def test_delete_jadwal_does_not_affect_dosen(client: TestClient, db_session: Session):
    """
    Test that deleting a Jadwal does not delete the associated Dosen.
    """
    jadwal1, _, _, dosen, _ = setup_jadwal_for_delete(db_session)

    # Delete jadwal
    delete_response = client.delete(f"/jadwal/{jadwal1.id}")
    assert delete_response.status_code == 204

    # Verify dosen still exists
    verify_dosen = db_session.query(DosenModel).filter_by(id=dosen.id).first()
    assert verify_dosen is not None
    assert verify_dosen.nidn == "5555555555"


def test_delete_jadwal_does_not_affect_mata_kuliah(
    client: TestClient, db_session: Session
):
    """
    Test that deleting a Jadwal does not delete the associated Mata Kuliah.
    """
    jadwal1, _, _, _, mk = setup_jadwal_for_delete(db_session)

    # Delete jadwal
    delete_response = client.delete(f"/jadwal/{jadwal1.id}")
    assert delete_response.status_code == 204

    # Verify mata kuliah still exists
    verify_mk = db_session.query(MataKuliahModel).filter_by(id=mk.id).first()
    assert verify_mk is not None
    assert verify_mk.kode_mk == "IF401"


def test_delete_multiple_jadwal(client: TestClient, db_session: Session):
    """
    Test deleting multiple Jadwal records sequentially.
    """
    jadwal1, jadwal2, jadwal3, _, _ = setup_jadwal_for_delete(db_session)

    # Delete first jadwal
    response1 = client.delete(f"/jadwal/{jadwal1.id}")
    assert response1.status_code == 204

    # Delete second jadwal
    response2 = client.delete(f"/jadwal/{jadwal2.id}")
    assert response2.status_code == 204

    # Verify only third jadwal remains
    verify_response = client.get("/jadwal/")
    assert verify_response.status_code == 200
    data = verify_response.json()
    assert len(data) == 1
    assert data[0]["id"] == jadwal3.id


def test_delete_jadwal_then_get_by_id_returns_empty(
    client: TestClient, db_session: Session
):
    """
    Test that getting a deleted Jadwal by ID returns empty list.
    """
    jadwal1, _, _, _, _ = setup_jadwal_for_delete(db_session)

    # Delete jadwal
    delete_response = client.delete(f"/jadwal/{jadwal1.id}")
    assert delete_response.status_code == 204

    # Try to get deleted jadwal
    get_response = client.get(f"/jadwal/?id={jadwal1.id}")
    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


def test_delete_jadwal_negative_id(client: TestClient, db_session: Session):
    """
    Test deleting Jadwal with negative ID returns 404 Not Found.
    """
    setup_jadwal_for_delete(db_session)

    response = client.delete("/jadwal/-1")
    assert response.status_code == 404


def test_delete_jadwal_zero_id(client: TestClient, db_session: Session):
    """
    Test deleting Jadwal with zero ID returns 404 Not Found.
    """
    setup_jadwal_for_delete(db_session)

    response = client.delete("/jadwal/0")
    assert response.status_code == 404


def test_delete_all_jadwal(client: TestClient, db_session: Session):
    """
    Test deleting all Jadwal records leaves database empty.
    """
    jadwal1, jadwal2, jadwal3, _, _ = setup_jadwal_for_delete(db_session)

    # Delete all jadwal
    client.delete(f"/jadwal/{jadwal1.id}")
    client.delete(f"/jadwal/{jadwal2.id}")
    client.delete(f"/jadwal/{jadwal3.id}")

    # Verify database is empty
    verify_response = client.get("/jadwal/")
    assert verify_response.status_code == 200
    assert len(verify_response.json()) == 0

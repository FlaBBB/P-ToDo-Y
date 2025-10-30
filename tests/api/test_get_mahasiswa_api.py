from datetime import date

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


def test_get_all_mahasiswa(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving all Mahasiswa records.
    """
    response = client.get("/mahasiswa/")
    assert response.status_code == 200
    assert len(response.json()) == 4
    assert response.json()[0]["nim"] == "2023000001"


def test_get_mahasiswa_by_id(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving a specific Mahasiswa record by ID.
    """
    mahasiswa1, _, _, _ = setup_mahasiswa_data
    response = client.get(f"/mahasiswa/?id={mahasiswa1.id}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nim"] == mahasiswa1.nim


def test_get_mahasiswa_by_nim(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving a specific Mahasiswa record by NIM.
    """
    _, mahasiswa2, _, _ = setup_mahasiswa_data
    response = client.get(f"/mahasiswa/?nim={mahasiswa2.nim}")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["nama"] == mahasiswa2.nama


def test_get_mahasiswa_by_nama_partial_match(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records by partial name match.
    """
    response = client.get("/mahasiswa/?nama=ali")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert (
        results[0]["nama"] == "Alice Wonderland"
    )  # Faker can sometimes produce similar names, assuming 'Alice' here.


def test_get_mahasiswa_by_kelas(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records by class.
    """
    response = client.get("/mahasiswa/?kelas=TI-3E")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert {m["nim"] for m in results} == {"2023000001", "2023000003"}


def test_get_mahasiswa_by_tempat_lahir(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records by birth place.
    """
    response = client.get("/mahasiswa/?tempat_lahir=Jakarta")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert {m["nim"] for m in results} == {"2023000001", "2024000004"}


def test_get_mahasiswa_by_tanggal_lahir(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records by birth date.
    """
    response = client.get("/mahasiswa/?tanggal_lahir=2000-01-15")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["nim"] == "2023000001"


def test_get_mahasiswa_with_pagination_limit(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records with a limit.
    """
    response = client.get("/mahasiswa/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_mahasiswa_with_pagination_limit_and_page(
    client: TestClient, setup_mahasiswa_data
):
    """
    Test retrieving Mahasiswa records with limit and page.
    """
    response = client.get(
        "/mahasiswa/?limit=2&page=2&order_by=nim&order=asc"
    )  # Order by nim for consistent results
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 2
    assert results[0]["nim"] == "2023000003"
    assert results[1]["nim"] == "2024000004"


def test_get_mahasiswa_with_ordering_asc(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records with ascending order by name.
    """
    response = client.get("/mahasiswa/?order_by=nama&order=asc")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    assert results[0]["nama"] == "Alice Wonderland"
    assert results[1]["nama"] == "Bob The Builder"
    assert results[2]["nama"] == "Charlie Chaplin"
    assert results[3]["nama"] == "David Copperfield"


def test_get_mahasiswa_with_ordering_desc(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records with descending order by name.
    """
    response = client.get("/mahasiswa/?order_by=nama&order=desc")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 4
    assert results[0]["nama"] == "David Copperfield"
    assert results[1]["nama"] == "Charlie Chaplin"
    assert results[2]["nama"] == "Bob The Builder"
    assert results[3]["nama"] == "Alice Wonderland"


def test_get_mahasiswa_not_found_by_id(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving a Mahasiswa record with a non-existent ID.
    """
    response = client.get("/mahasiswa/?id=999")
    assert response.status_code == 200  # GET operations return empty list if not found
    assert len(response.json()) == 0


def test_get_mahasiswa_not_found_by_nim(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving a Mahasiswa record with a non-existent NIM.
    """
    response = client.get("/mahasiswa/?nim=9999999999")
    assert response.status_code == 200  # GET operations return empty list if not found
    assert len(response.json()) == 0


def test_get_mahasiswa_invalid_date_format(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa with an invalid date format for tanggal_lahir.
    """
    response = client.get("/mahasiswa/?tanggal_lahir=2000/01/15")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]


def test_get_mahasiswa_combined_filters(client: TestClient, setup_mahasiswa_data):
    """
    Test retrieving Mahasiswa records with multiple filters combined.
    """
    response = client.get("/mahasiswa/?kelas=TI-3E&tempat_lahir=Jakarta")
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["nim"] == "2023000001"

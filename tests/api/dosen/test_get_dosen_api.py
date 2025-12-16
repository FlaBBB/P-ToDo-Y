from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.repositories.database.models.dosen import DosenModel


def test_get_all_dosen(client: TestClient, db_session: Session):
    """
    Test getting all Dosen records.
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Prof. Jane Smith",
        email="jane.smith@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()

    response = client.get("/dosen/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nidn"] == "0123456789"
    assert data[1]["nidn"] == "9876543210"


def test_get_dosen_by_id(client: TestClient, db_session: Session):
    """
    Test getting a Dosen by ID.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()
    db_session.refresh(dosen)

    response = client.get(f"/dosen/?id={dosen.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == dosen.id
    assert data[0]["nidn"] == "0123456789"


def test_get_dosen_by_nidn(client: TestClient, db_session: Session):
    """
    Test getting a Dosen by NIDN.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()

    response = client.get("/dosen/?nidn=0123456789")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nidn"] == "0123456789"


def test_get_dosen_by_nama(client: TestClient, db_session: Session):
    """
    Test getting Dosen by nama (partial match).
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="1111111111",
        nama="Dr. John Smith",
        email="john.smith@university.ac.id",
    )
    dosen3 = DosenModel(
        nidn="2222222222",
        nama="Prof. Jane Doe",
        email="jane.doe@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2, dosen3])
    db_session.commit()

    response = client.get("/dosen/?nama=John")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("John" in dosen["nama"] for dosen in data)


def test_get_dosen_by_email(client: TestClient, db_session: Session):
    """
    Test getting a Dosen by email.
    """
    # Insert test data
    dosen = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    db_session.add(dosen)
    db_session.commit()

    response = client.get("/dosen/?email=john.doe@university.ac.id")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "john.doe@university.ac.id"


def test_get_dosen_not_found(client: TestClient, db_session: Session):
    """
    Test getting Dosen when no records match returns empty list.
    """
    response = client.get("/dosen/?id=999")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_get_dosen_with_pagination(client: TestClient, db_session: Session):
    """
    Test getting Dosen with pagination.
    """
    # Insert test data
    for i in range(5):
        dosen = DosenModel(
            nidn=f"012345678{i}",
            nama=f"Dr. Dosen {i}",
            email=f"dosen{i}@university.ac.id",
        )
        db_session.add(dosen)
    db_session.commit()

    response = client.get("/dosen/?limit=2&page=1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_get_dosen_with_ordering_asc(client: TestClient, db_session: Session):
    """
    Test getting Dosen with ordering (ascending).
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. Zack",
        email="zack@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Dr. Alice",
        email="alice@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()

    response = client.get("/dosen/?order_by=nama&order=asc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nama"] == "Dr. Alice"
    assert data[1]["nama"] == "Dr. Zack"


def test_get_dosen_with_ordering_desc(client: TestClient, db_session: Session):
    """
    Test getting Dosen with ordering (descending).
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. Zack",
        email="zack@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Dr. Alice",
        email="alice@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()

    response = client.get("/dosen/?order_by=nama&order=desc")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["nama"] == "Dr. Zack"
    assert data[1]["nama"] == "Dr. Alice"


def test_get_dosen_multiple_filters(client: TestClient, db_session: Session):
    """
    Test getting Dosen with multiple filters.
    """
    # Insert test data
    dosen1 = DosenModel(
        nidn="0123456789",
        nama="Dr. John Doe",
        email="john.doe@university.ac.id",
    )
    dosen2 = DosenModel(
        nidn="9876543210",
        nama="Dr. John Smith",
        email="john.smith@university.ac.id",
    )
    db_session.add_all([dosen1, dosen2])
    db_session.commit()

    response = client.get("/dosen/?nama=John&email=john.doe@university.ac.id")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == "john.doe@university.ac.id"


def test_get_dosen_empty_database(client: TestClient, db_session: Session):
    """
    Test getting Dosen from empty database returns empty list.
    """
    response = client.get("/dosen/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0
    assert data == []

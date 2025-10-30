import os
import sys
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.application.usecases.mahasiswa import MahasiswaService
from src.dependencies import get_mahasiswa_service as get_mahasiswa_service_prod
from src.infrastructure.app import app
from src.repositories.database.core import Base
from src.repositories.database.mahasiswa import MahasiswaRepository

# ----------------------------------------------------------------------
# 1. Setup In-Memory SQLite Database for Testing
# ----------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(name="db_session")
def db_session_fixture() -> Generator[Session, None, None]:
    """
    Creates a new database session for each test,
    clears the tables, creates them again, and yields the session.
    """
    Base.metadata.drop_all(bind=engine)  # Drop existing tables
    Base.metadata.create_all(bind=engine)  # Create new tables
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session  # Provide the session for the test

    session.close()
    transaction.rollback()  # Rollback all changes
    connection.close()


# ----------------------------------------------------------------------
# 2. Override Dependencies for Testing
# ----------------------------------------------------------------------
@pytest.fixture(name="override_get_db_session")
def override_get_db_session_fixture(
    db_session: Session,
) -> Generator[Session, None, None]:
    """
    Overrides the get_db_session dependency to use the test database session.
    """
    yield db_session


@pytest.fixture(name="override_get_mahasiswa_service")
def override_get_mahasiswa_service_fixture(db_session: Session) -> MahasiswaService:
    """
    Overrides the get_mahasiswa_service dependency to use the test repository
    with the test database session.
    """
    repository = MahasiswaRepository(session_db=db_session)
    service = MahasiswaService(mahasiswa_repo=repository)
    return service


# ----------------------------------------------------------------------
# 3. Create a TestClient Instance
# ----------------------------------------------------------------------
@pytest.fixture(name="client")
def client_fixture(
    override_get_db_session: Generator[Session, None, None],
    override_get_mahasiswa_service: MahasiswaService,
):
    """
    Provides a TestClient for making requests to the FastAPI application.
    It overrides the dependencies to ensure tests use the test database.
    """
    # Override the dependencies in the main app
    app.dependency_overrides[Base.metadata.create_all] = (
        lambda: None
    )  # Prevent actual table creation on app startup
    app.dependency_overrides[get_mahasiswa_service_prod] = (
        lambda: override_get_mahasiswa_service
    )

    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides after the test
    app.dependency_overrides = {}

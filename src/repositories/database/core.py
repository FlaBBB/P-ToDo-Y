from abc import abstractmethod
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from src.config import Config  # Import the Config class

# Initialize Config to load environment variables
config = Config()

engine: Engine = create_engine(
    config.DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    @abstractmethod
    def to_entity(self):
        raise NotImplementedError("Subclasses must implement to_entity method")


def get_db_session() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

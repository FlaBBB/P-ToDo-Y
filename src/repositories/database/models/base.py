from sqlalchemy.orm import DeclarativeBase
from abc import abstractmethod


class Base(DeclarativeBase):
    @abstractmethod
    def to_entity(self):
        raise NotImplementedError("Subclasses must implement to_entity method")

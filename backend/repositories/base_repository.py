from typing import TypeVar, Generic, Optional, Type
from sqlmodel import Session, select, SQLModel

T = TypeVar("T", bound=SQLModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], session: Session):
        self.model = model
        self.session = session

    def get_by_id(self, id: int) -> Optional[T]:
        return self.session.get(self.model, id)

    def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        statement = select(self.model).offset(offset).limit(limit)
        return list(self.session.exec(statement).all())

    def add(self, entity: T) -> None:
        self.session.add(entity)

    def delete(self, entity: T) -> None:
        self.session.delete(entity)

    def refresh(self, entity):
        self.session.refresh(entity)

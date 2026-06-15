import os
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

from backend.core.config import settings

database_url = settings.database_url
if database_url.startswith("sqlite:///./"):
    db_name = database_url.split("sqlite:///./")[1]
    db_path = os.path.join(os.path.dirname(__file__), db_name)
    database_url = f"sqlite:///{db_path}"

connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
engine = create_engine(database_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

def get_uow():
    from backend.uow.unit_of_work import UnitOfWork
    return UnitOfWork()

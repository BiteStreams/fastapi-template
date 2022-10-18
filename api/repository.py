from functools import lru_cache

from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base


SQL_BASE = declarative_base()


@lru_cache(maxsize=None)
def get_engine(connection_string = "postgresql://postgres:test@db:5432/postgres"):
    return create_engine(connection_string, pool_pre_ping=True)


class TodoInDB(SQL_BASE):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(length=128), nullable=False)
    value = Column(String(length=128), nullable=False)


@dataclass
class Todo:
    key: str
    value: str


class TodoRepository:
    def __init__(self, session):
        self.session: Session = session

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value: str, exc_traceback: str) -> None:
        if exc_type is not None:
            self.session.rollback()
            return

        error = None

        try:
            self.session.commit()
        except DatabaseError as error:
            self.session.rollback()

        if error:
            raise ValueError("A storage error occurred") from error

    def save(self, todo: Todo):
        self.session.add(TodoInDB(key=todo.key, value=todo.value))

    def get_by_key(self, key: str):
        instance = self.session.query(TodoInDB) \
            .filter(TodoInDB.key == key) \
            .first()

        if instance:
            return Todo(instance.key, instance.value)


def create_todo_repository():
    session = sessionmaker(bind=get_engine())()
    repository = TodoRepository(session)

    try:
        yield repository
    except Exception as error:
        session.rollback()

        raise error
    finally:
        session.close()


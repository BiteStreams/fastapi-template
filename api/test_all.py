import pytest

from .repository import TodoRepository, Todo, get_engine, SQL_BASE
from sqlalchemy.orm import sessionmaker


@pytest.mark.unit
def test_sanity():
    assert 1 != 0


@pytest.mark.integration
def test_repository():
    engine = get_engine("postgresql://postgres:test@ci_db:5432/postgres")
    session = sessionmaker(bind=engine)()

    SQL_BASE.metadata.create_all(engine)

    repository = TodoRepository(session)

    with repository as r:
        r.save(Todo("testkey", "testvalue"))

    todo = r.get_by_key("testkey")
    assert todo.value == "testvalue"

    session.close()

    session = sessionmaker(bind=engine)()
    for table in SQL_BASE.metadata.tables.keys():
        session.execute(f"TRUNCATE TABLE {table} CASCADE")

    session.commit()
    session.close()

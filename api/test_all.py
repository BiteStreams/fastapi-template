import os
import time

import alembic.config
import pytest
from sqlalchemy.orm import sessionmaker

from api.repository import SQL_BASE, Todo, TodoRepository, get_engine


@pytest.mark.unit
def test_sanity():
    assert 1 != 0


@pytest.mark.integration
def test_repository():
    os.environ["DB_STRING"] = "postgresql://postgres:test@ci_db:5432/postgres"
    repository = get_repo()

    with repository as r:
        r.save(Todo("testkey", "testvalue"))

    todo = r.get_by_key("testkey")
    assert todo.value == "testvalue"

    repository._session.close()

    cleanup_database()


def cleanup_database():
    session = sessionmaker(bind=get_engine())()

    for table in SQL_BASE.metadata.tables.keys():
        session.execute(f"TRUNCATE TABLE {table} CASCADE")

    session.commit()
    session.close()


def get_repo():
    time.sleep(1)
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)

    return TodoRepository(sessionmaker(bind=get_engine())())

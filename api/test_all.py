import os
import time

import alembic.config
import pytest
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from api.main import app
from api.repository import SQL_BASE, Todo, TodoRepository, get_engine


@pytest.mark.unit
def test_sanity():
    assert 1 != 0


@pytest.mark.integration
def test_repository():
    repository = get_repo()

    with repository as r:
        r.save(Todo(key="testkey", value="testvalue"))

    todo = r.get_by_key("testkey")
    assert todo.value == "testvalue"

    repository._session.close()

    cleanup_database()


@pytest.mark.integration
def test_api():
    time.sleep(1)
    client = TestClient(app)
    response = client.post("testkey?value=testvalue")

    assert response.status_code == 200
    response = client.get("testkey")

    assert response.status_code == 200
    assert response.json() == {"key": "testkey", "value": "testvalue"}


def cleanup_database():
    session = sessionmaker(bind=get_engine())()

    for table in SQL_BASE.metadata.tables.keys():
        session.execute(f"TRUNCATE TABLE {table} CASCADE")

    session.commit()
    session.close()


def get_repo():
    os.environ["DB_STRING"] = "postgresql://postgres:test@ci_db:5432/postgres"
    time.sleep(1)
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)

    return TodoRepository(sessionmaker(bind=get_engine())())

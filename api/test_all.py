import os
import time

import alembic.config
import pytest
from sqlalchemy.exc import DataError, IntegrityError
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from api.main import app
from api.repository import SQL_BASE, SQLTodoRepository, Todo, TodoFilter, get_engine


@pytest.mark.unit
def test_sanity():
    assert 1 != 0


@pytest.fixture
def todo_repository():
    time.sleep(1)
    alembicArgs = ["--raiseerr", "upgrade", "head"]
    alembic.config.main(argv=alembicArgs)

    engine = get_engine(os.getenv("DB_STRING"))
    session = sessionmaker(bind=engine)()

    yield SQLTodoRepository(session)

    session.close()

    sessionmaker(bind=engine, autocommit=True)().execute(
        ";".join([f"TRUNCATE TABLE {t} CASCADE" for t in SQL_BASE.metadata.tables.keys()])
    )


@pytest.mark.integration
def test_repository(todo_repository: SQLTodoRepository):
    with todo_repository as r:
        r.save(Todo(key="testkey", value="testvalue"))

    todo = r.get_by_key("testkey")
    assert todo.value == "testvalue"

    with pytest.raises(IntegrityError):
        with todo_repository as r:
            r.save(Todo(key="testkey", value="not allowed: unique todo keys!"))

    with pytest.raises(DataError):
        with todo_repository as r:
            r.save(Todo(key="too long", value=129 * "x"))


@pytest.mark.integration
def test_repository_filter(todo_repository: SQLTodoRepository):
    with todo_repository as r:
        r.save(Todo(key="testkey", value="testvalue"))
        r.save(Todo(key="abcde", value="v"))

    todos = r.get(TodoFilter(key_contains="test"))
    assert len(todos) == 1
    assert todos[0].value == "testvalue"

    todos = r.get(TodoFilter(key_contains="abcde"))
    assert len(todos) == 1
    assert todos[0].value == "v"

    assert len(r.get(TodoFilter(key_contains="e"))) == 2
    assert len(r.get(TodoFilter(key_contains="e", limit=1))) == 1
    assert len(r.get(TodoFilter(value_contains="v"))) == 2
    assert len(r.get(TodoFilter(done=True))) == 0


@pytest.mark.integration
def test_api():
    time.sleep(1)
    client = TestClient(app)
    response = client.post("/create/testkey?value=testvalue")

    assert response.status_code == 201
    response = client.get("/get/testkey")

    assert response.status_code == 200
    assert response.json() == {"key": "testkey", "value": "testvalue", "done": False}

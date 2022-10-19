from typing import Optional

from fastapi import Depends, FastAPI

from api.repository import Todo, TodoRepository, create_todo_repository

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/{key}")
async def create(key: str, value: str, todo_repository: TodoRepository = Depends(create_todo_repository)):
    with todo_repository as t:
        t.save(Todo(key=key, value=value))

    return {"status": "success"}


@app.get("/{key}", response_model=Optional[Todo])
async def get(key: str, todo_repository: TodoRepository = Depends(create_todo_repository)):
    with todo_repository as t:
        return t.get_by_key(key)

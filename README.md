# Fastapi Template

A FastAPI project template using Make, Docker Compose and Github Actions.
This includes a SQLAlchemy+Alembic integration and an integration test setup.
This repository was used for a presentation at Shark Tech Talks.


## Tooling

The development tools used include:
- Make
- Docker Compose
- Github Actions

Regarding the Python api, here we used:
- Poetry (package management)
- FastAPI
- SQLAlchemy
- Alembic


## Tests

The tests are containerized and the Docker setup can be found in the `.ci/` folder.
They are written using Pytest.


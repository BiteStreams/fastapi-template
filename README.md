# Fastapi Project Template


A FastAPI project template using Make, Docker Compose and Github Actions,
that includes **SQLAlchemy**, **Alembic** and an integration test setup.

[![Code Integration](https://github.com/bitestreams/fastapi-template/actions/workflows/code-integration.yml/badge.svg)](https://github.com/alcoat/fastapi-template/actions/workflows/code-integration.yml)

##  Installation

### Requirements
The only requirements to develop are **Docker** and **Make**.
Docker makes it easy to get started and enables easier switching between projects, operating systems and machines.

---

To install a local copy of the python environment (to get code-completion for example),
you have to have **Poetry** installed and create a poetry environment
by running `poetry install` at the root of the project.

### Makefile

---
The Makefile is the 'entrypoint' for the tools in this structure,
such that you can easily run different commands without remembering the exact arguments.
Run `make help` to get an overview of the available commands:
```sh
$ make help
up: 
 Run the application
done: lint test 
 Prepare for a commit
test: utest itest  
 Run unit and integration tests
check: 
 Check the code base
lint: 
 Check the code base, and fix it
clean_test:  
 Clean up test containers
migrations: 
 Generate a migration using alembic
migrate: 
 Run migrations upgrade using alembic
downgrade: 
 Run migrations downgrade using alembic
help: 
 Display this help message
```

---

To start up the project locally you first clone the project, and then run the following command in the cloned directory:
```sh
$ git clone https://github.com/BiteStreams/fastapi-template.git
$ cd fastapi-template
$ make up
```
Then to update the schema using alembic, in another shell:
```sh
$ make migrate
```
**That's it**. The app is set up and should be running at [localhost:5000/docs](localhost:5000/docs).
Code changes are automatically detected using a docker volume.

### Tests

---

The tests are containerized and the Docker setup can be found in the `.ci/` folder.
They are written using Pytest.
You can run the tests using:
```bash
$ make test
```
This runs the integration & unit tests. If you want to run them separately, use `make itest` to run the integration tests and `make utest` to run the unit tests.


## Further reading

To read about the benefits of using this template,
check out [our blog post](https://bitestreams.com/blog/fastapi_template/).

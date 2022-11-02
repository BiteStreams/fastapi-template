# Fastapi Template

A FastAPI project template using Make, Docker Compose and Github Actions.
This includes a SQLAlchemy+Alembic integration and an integration test setup.

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


##  Development
Development in this setup is done using Docker, this makes it very easy to get started and enables easier switching between projects, operating systems and machines.

The only requirements to develop are:
- Docker
- Make

To install a local copy of the python environment (to get code-completion for example) you can install the poetry environment (given you have the correct python version and poetry installed
) with `$ poetry install` in the root dir of the project.

### Makefile
The Makefile is the 'entrypoint' for the tools in this structure, such that you can easily run different commands without remembering the exact arguments, run:
```sh
$ make help
```
To get an overview of the available commands, output:
```txt
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

To start up the project locally you first clone the project, and then run the following command in the cloned directory:
```shell
$ make up
```
Then to update the schema using alembic, in another shell:
```shell
$ make migrate
```
**Thats it**, now the app is running and works and is reachable on [localhost:5000/docs](localhost:5000/docs). 

Code changes are automatically detected using a docker-volume.

### Tests

The tests are containerized and the Docker setup can be found in the `.ci/` folder.
They are written using Pytest.
You can run the tests using:
```shell
$ make test
```
This runs the integration & unit tests. If you want to run them separately, use `make itest` to run the integration tests and `make utest` to run the unit tests.

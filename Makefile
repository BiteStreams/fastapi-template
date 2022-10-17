SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c

export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

targets: help

build: ## Build the application
	docker build -f api/Dockerfile . --tag $(APP_IMAGE_URI) --tag $(APP_IMAGE_URI_LATEST) --target prod --build-arg BUILDKIT_INLINE_CACHE=1 --cache-from $(APP_IMAGE_URI_LATEST)

up: ## Run the application
	docker-compose up --build api

check: ## Check the code base
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) black ./$(cdir) --check --diff
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) isort ./$(cdir) --check --diff
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) mypy ./$(cdir) --ignore-missing-imports

lint: ## Check the code base, and fix it
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) black ./$(cdir)
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) isort ./$(cdir)
	docker run -v $(PWD):/app/$(cdir) $(CHECK_IMAGE_URI) mypy ./$(cdir) --ignore-missing-imports

TEST_FLAGS =
ifeq ($(v), 1)
	TEST_FLAGS = --log-cli-level='ERROR' -s -vv
endif

TEST_PATH = .
ifneq ($(p),)
	TEST_PATH = $(p)
endif

done: lint test ## Prepare for a commit

test: utest itest ## Run unit and integration tests

utest: ## Run unit tests
	docker-compose -f base.yml -f .ci/docker-compose.yml down --volumes --remove-orphans
	docker-compose -f base.yml -f .ci/docker-compose.yml run --rm unit pytest -m unit $(TEST_FLAGS) $(TEST_PATH)

itest: ## Run integration tests
	docker-compose -f base.yml -f .ci/docker-compose.yml down --volumes --remove-orphans
	docker-compose -f base.yml -f .ci/docker-compose.yml run --rm integration pytest -m integration $(TEST_FLAGS) $(TEST_PATH)


## Migrations


migrations: ## Generate a migration using alembic
ifeq ($(m),)
	@echo "Specify a message with m={message} and a rev-id with revid={revid} (e.g. 0001 etc.)"; exit 1
else ifeq ($(revid),)
	@echo "Specify a message with m={message} and a rev-id with revid={revid} (e.g. 0001 etc.)"; exit 1
else
	docker-compose run api alembic revision --autogenerate -m "$(m)" --rev-id="$(revid)"
endif

migrate: ## Run migrations upgrade using alembic
	docker-compose run --rm api alembic upgrade head

downgrade: ## Run migrations downgrade using alembic
	docker-compose run --rm api alembic downgrade -1

help: ## Display this help message
	@awk -F '##' '/^[a-z_]+:[a-z ]+##/ { print "\033[34m"$$1"\033[0m" "\n" $$2 }' Makefile

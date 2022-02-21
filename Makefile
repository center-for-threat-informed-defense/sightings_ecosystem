#
# See `make help` for a list of all available commands.
#

APP_NAME := sightings
VENV := .venv
BIN := $(VENV)/bin
PY_VERSION := python3.8
TIMESTAMP := $(shell date -u +"%Y%m%d_%H%M%S")
GIT_HASH := $(shell git rev-parse --short HEAD)

.DEFAULT_GOAL := help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# the aliasing for the venv target is done primarily for readability
$(VENV): $(BIN)/activate

venv: $(VENV)  ## build python venv

$(BIN)/activate:
	$(PY_VERSION) -m venv --prompt $(APP_NAME) $(VENV)

.PHONY: install
install: venv  upgrade-pip ## Install Python dependencies
	./$(BIN)/python -m pip install -r requirements/pipeline-requirements.txt
	./$(BIN)/python -m pip install -r requirements/analysis-requirements.txt
	./$(BIN)/python -m pip install -r requirements/pipeline-requirements-ci.txt

.PHONY: upgrade-pip
upgrade-pip: venv  ## Upgrade pip and related
	./$(BIN)/python -m pip install --upgrade pip wheel setuptools pip-tools

.PHONY: build-container
build-containers: venv ## Build container images
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml build

.PHONY: clean
clean: ## Clean up pycache files
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -type d -delete

.PHONY: clean-all
clean-all: clean ## Clean up venv and tox if necessary, in addition to standard clean
	find . \( -name ".tox" -o -name "$(VENV)" -o -name "*.egg-info"  \) -type d -prune -exec rm -rf {} +
	find ./src -name '*.egg' -delete
	rm -f coverage.xml

.PHONY: venv-activate
venv-activate: venv ## Activate venv
	@echo "Activate your virtualenv by running the following command: "
	@echo "source $(BIN)/activate"

.PHONY: venv-deactivate
venv-deactivate: ## Deactivate venv
	@echo "Activate your virtualenv by running the following command: "
	@echo "source deactivate"

.PHONY: start-analysis
start-analysis: ## Start analysis service and dependencies
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml --profile analysis up -d

.PHONY: start-pipeline
start-pipeline: ## Start pipeline service and dependencies
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml --profile pipeline up -d

.PHONY: start-analysis-and-pipeline
start-analysis-and-pipeline: ## Start analysis and pipeline services and dependencies
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml --profile analysis --profile pipeline up -d

.PHONY: start-pgadmin
start-pgadmin: ## Start pgadmin
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml --profile pgadmin up -d

.PHONY: stop
stop: ## Stop all services
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml down

.PHONY: stop-pgadmin
stop-pgadmin: ## Stop pgadmin
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml --profile pgadmin down pgadmin

.PHONY: logs
logs: ## View logs for analysis service and dependencies
	DOCKER_BUILDKIT=1 docker-compose -f docker-compose.yml logs

.PHONY: test
test: install ## Run tests
	./$(BIN)/pytest --cov=src/pipeline --cov=src/analysis --cov=src/validator --cov-report=xml --flake8

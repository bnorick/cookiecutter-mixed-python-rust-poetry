PACKAGE := {{ cookiecutter.package_name }}
PACKAGE_DIR := src/python/${PACKAGE}
MODULES := $(wildcard $(PACKAGE_DIR)/*.py)

# MAIN TASKS ##################################################################

.PHONY: all
all: doctor format check test mkdocs ## Run all tasks that determine CI status

.PHONY: dev
dev: install  ## Continuously run all CI tasks when files chanage
	poetry run ptw

.PHONY: shell
shell: install
	poetry run ipython --ipython-dir=notebooks

.PHONY: demo
demo: install
	poetry run nbstripout notebooks/*.ipynb
	poetry run jupyter notebook --notebook-dir=notebooks --browser=firefox

# SYSTEM DEPENDENCIES #########################################################

.PHONY: bootstrap
bootstrap: ## Attempt to install system dependencies
	asdf plugin add python || asdf plugin update python
	asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git || asdf plugin update poetry
	asdf install

.PHONY: doctor
doctor: ## Confirm system dependencies are available
	bin/verchew

# PROJECT DEPENDENCIES ########################################################

DEPENDENCIES := target/.poetry-$(shell bin/checksum pyproject.toml poetry.lock)

.PHONY: install
install: $(DEPENDENCIES) .cache ## Install project dependencies

$(DEPENDENCIES): poetry.lock
	@ rm -rf $(VIRTUAL_ENV)/.poetry-*
	@ poetry config virtualenvs.in-project true
	poetry install
	@ touch $@

poetry.lock: pyproject.toml
	poetry lock --no-update
	@ touch $@

.cache:
	@ mkdir -p .cache

# CHECKS ######################################################################

.PHONY: format
format: install
	poetry run ruff ${PACKAGE_DIR} tests/python
	poetry run black $(PACKAGE_DIR) tests/python
	@ echo

.PHONY: check
check: install format  ## Run formaters, linters, and static analysis
	poetry run mypy ${PACKAGE_DIR} tests/python
	poetry run deptry ${PACKAGE_DIR} tests/python

# TESTS #######################################################################

.PHONY: test
test: install  ## Run unit and integration tests
	poetry run pytest tests/python --random --doctest-modules

.PHONY: test-repeat
test-repeat: install
	poetry run pytest tests/python --count=5 --random --doctest-modules --exitfirst

# RELEASE #####################################################################

DIST_FILES := dist/*.tar.gz dist/*.whl

.PHONY: dist
dist: install $(DIST_FILES)
$(DIST_FILES): $(MODULES) pyproject.toml
	rm -f $(DIST_FILES)
	poetry build

.PHONY: upload
upload: dist  ## Upload the current version to PyPI
	git diff --name-only --exit-code
	poetry publish
	bin/open https://pypi.org/project/$(PACKAGE)


# CLEANUP #####################################################################

.PHONY: clean
clean:  ## Delete all generated and temporary files
	rm -rf .venv
	rm -rf dist
	rm -rf target
	rm -rf src/rust/target

# HELP ########################################################################

.PHONY: help
help: install
	@ grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help

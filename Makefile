BIN_DIR ?= $(PWD)/tests/bin
PYTHON_VENV ?= $(PWD)/.venv
BUILD_ROOT ?= $(PWD)/build

run-python-venv=(. $(PYTHON_VENV)/bin/activate && $1)

venv:
	python3 -m venv $(PYTHON_VENV)
	chmod +x $(PYTHON_VENV)/bin/activate

activate-path:
	@echo "$(PYTHON_VENV)/bin/activate"

.PHONY: install-deps
install-deps:
	$(call run-python-venv, pip3 install -r requirements.txt)

.PHONY: update-deps
update-deps:
	$(call run-python-venv, pip-compile requirements.in > requirements.txt)

.PHONY: download-binaries
download-binaries:
	mkdir -p $(BIN_DIR)
	cd $(BIN_DIR) && curl -L -O https://github.com/tabulapdf/tabula-java/releases/download/v1.0.4/tabula-1.0.4-jar-with-dependencies.jar
	cd $(BIN_DIR) && curl -L -O http://archive.apache.org/dist/tika/tika-app-1.24.1.jar

.PHONY: setup
setup: venv install-deps download-binaries
	$(call run-python-venv, pre-commit install)

.PHONY: check
check:
	$(call run-python-venv, ruff check **/*.py)

.PHONY: format
format:
	$(call run-python-venv, pre-commit run --files **/*.py)

.PHONY: test
test:
	$(call run-python-venv, python -m unittest discover -f --start-directory=tests --pattern "*.py")

.PHONY: coverage
coverage:
	$(call run-python-venv, coverage erase)
	$(call run-python-venv, coverage run -m unittest discover -f --start-directory=tests --pattern "*.py")
	$(call run-python-venv, coverage report -m)

.PHONY: build
build:
	mkdir -p $(BUILD_ROOT)
	python3 setup.py install --root=$(BUILD_ROOT) --prefix=/usr

.PHONY: publish
publish:
	$(call run-python-venv, python setup.py upload)

BIN_DIR ?= $(PWD)/tests/bin
PYTHON_VENV ?= $(PWD)/.venv
BUILD_ROOT ?= $(PWD)/build
ISORT_ARGS := --combine-star --combine-as --order-by-type --thirdparty scrapy --multi-line 3 --trailing-comma --force-grid-wrap 0 --use-parentheses --line-width 88

run-python-venv=(. $(PYTHON_VENV)/bin/activate && $1)

pyenv:
	python3 -m venv $(PYTHON_VENV)

.PHONY: install-deps
install-deps:
	$(call run-python-venv, pip3 install -r requirements.txt)

.PHONY: download-binaries
download-binaries:
	mkdir -p $(BIN_DIR)
	cd $(BIN_DIR) && curl -L -O https://github.com/tabulapdf/tabula-java/releases/download/v1.0.4/tabula-1.0.4-jar-with-dependencies.jar
	cd $(BIN_DIR) && curl -L -O http://archive.apache.org/dist/tika/tika-app-1.24.1.jar

.PHONY: setup
setup: pyenv install-deps download-binaries

.PHONY: black
black:
	$(call run-python-venv, black $(PWD))

.PHONY: isort
isort:
	$(call run-python-venv, python -m isort --apply $(ISORT_ARGS) **/*.py)

.PHONY: check
check:
	$(call run-python-venv, flake8 **/*.py)

.PHONY: format
format: black isort


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

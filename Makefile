IMAGE_NAMESPACE ?= serenata
IMAGE_NAME ?= querido-diario-toolbox
IMAGE_TAG ?= latest
POD_NAME ?= querido-diario-toolbox-testing
BIN_DIR ?= $(PWD)/bin


run-command=(podman run --rm -ti \
	--volume $(PWD):/mnt/code:rw \
	--pod $(POD_NAME) \
	--env PYTHONPATH=/mnt/code \
	--env POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	--env POSTGRES_USER=$(POSTGRES_USER) \
	--env POSTGRES_DB=$(POSTGRES_DB) \
	--env POSTGRES_HOST=$(POSTGRES_HOST) \
	--env POSTGRES_PORT=$(POSTGRES_PORT) \
	--user=$(UID):$(UID) $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) $1)


.PHONY: black
black:
	podman run --rm -ti --volume $(PWD):/mnt/code:rw \
		--env PYTHONPATH=/mnt/code \
		--user=$(UID):$(UID) $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) \
		black .

.PHONY: build
build:
	podman build --tag $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) \
		-f Dockerfile $(PWD)

.PHONY: destroy
destroy:
	podman rmi --force $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG)

destroy-pod:
	podman pod rm --force --ignore $(POD_NAME)

create-pod: destroy-pod
	podman pod create --name $(POD_NAME)

.PHONY: test
test: create-pod retest

.PHONY: retest
retest:
	$(call run-command, python -m unittest -f tests)


shell:
	podman run --rm -ti --volume $(PWD):/mnt/code:rw \
	--env PYTHONPATH=/mnt/code \
	--user=$(UID):$(UID) $(IMAGE_NAMESPACE)/$(IMAGE_NAME):$(IMAGE_TAG) bash

.PHONY: coverage
coverage: create-pod
	$(call run-command, coverage erase)
	$(call run-command, coverage run -m unittest tests)
	$(call run-command, coverage report -m)

.PHONY: download-binaries
download-binaries:
	#wget https://github.com/tabulapdf/tabula-java/releases/download/v1.0.4/tabula-1.0.4-jar-with-dependencies.jar
	mkdir -p $(BIN_DIR)
	curl -o $(BIN_DIR)/tika-app-1.24.jar  http://archive.apache.org/dist/tika/tika-app-1.24.jar

.PHONY: setup
setup: download-binaries build

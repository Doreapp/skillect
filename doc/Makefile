PYTHON=python3

SRC_DIR=src
DOCKER_IMAGE=skillect-doc
DOCKER_RUN=docker run \
 -u $(shell id -u):$(shell id -g) \
 -v $(shell pwd)/$(SRC_DIR):/work/$(SRC_DIR)

SERVE_PORT=8000

.PHONY: html

all: html

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: 		## Build docker image
	docker build -t $(DOCKER_IMAGE) .

test:
	A=erty \
		echo $$(A)


clean: 		## Clean the directory
	@rm -rf html
	@find . -type d -name __pycache__ -exec rm -rf {} \; || true
	@find . -type f -name "*.pyc" -exec rm -rf {} \; || true
	@find . -type f -name "*.pyo" -exec rm -rf {} \; || true

_interactive: # Enter the docker container in interactive mode
_interactive: build
	$(DOCKER_RUN) --entrypoint /bin/bash -i $(OPTIONS) -t $(DOCKER_IMAGE)

html:		## Build HTML version of the documentation
html:
	sphinx-build -b html $(SRC_DIR) html/

docker_html:	## Build HTML using docker
docker_html: build
	mkdir -p $(shell pwd)/html
	$(DOCKER_RUN) $(OPTIONS) \
		-v $(shell pwd)/html:/work/html \
		-t $(DOCKER_IMAGE) \
		html

serve:		## Serve the HTML documentation
serve:
	$(PYTHON) -m http.server -d html $(SERVE_PORT)

docker_serve:	## Serve the HTML documentation using docker
docker_serve: build
	mkdir -p $(shell pwd)/html
	$(DOCKER_RUN) $(OPTIONS) \
		-v $(shell pwd)/html:/work/html \
		-p $(SERVE_PORT):$(SERVE_PORT) \
		-i -t $(DOCKER_IMAGE) \
		serve

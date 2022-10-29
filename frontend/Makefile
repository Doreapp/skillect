PORT=3000
DOCKER_IMAGE=skillect-frontend
DOCKER_RUN=docker run \
 -u $(shell id -u):$(shell id -g) \
 -v $(PWD)/src/:/app/src/ \
 -p $(PORT):$(PORT)

all: build dev

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: 		## Build docker image
build:
	docker build -t $(DOCKER_IMAGE) $(OPTIONS) .

run_%: 		## Run 'npm run %'
run_%:
	$(DOCKER_RUN) -t $(DOCKER_IMAGE) run $(shell echo $@ | cut -d _ -f 2)

_start: 	# Run 'npm start'
_start:
	$(DOCKER_RUN) -i -t $(DOCKER_IMAGE) start

dev: 		## Start the development server
dev: build _start

format: 	## Reformat the code
format: build run_format

lint: 		## Check code format
lint: build run_lint

_interactive: # Enter the docker image interactivelly
_interactive: build
	$(DOCKER_RUN) -i --entrypoint /bin/bash -t $(DOCKER_IMAGE)

_node_modules: # Force node_nodules update
	mkdir -p node_modules
	$(DOCKER_RUN) \
		-v $(PWD)/node_modules:/app/node_modules \
		-t $(DOCKER_IMAGE) install

node_modules: 	## Build and return node_modules directory using docker
node_modules: build _node_modules

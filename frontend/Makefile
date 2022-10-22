PORT=3000
DOCKER_IMAGE=skillect-frontend
DOCKER_RUN=docker run \
 -u $(shell id -u):$(shell id -g) \
 -v $(PWD)/src/:/app/src/ \
 -p $(PORT):$(PORT)

all: build dev

build: ## Build docker image
build:
	docker build -t $(DOCKER_IMAGE) $(OPTIONS) .

_start: # Run 'npm start'
_start:
	$(DOCKER_RUN) -i -t $(DOCKER_IMAGE) start

dev: ## Start the development server
dev: build _start

_interactive: # Enter the docker image interactivelly
_interactive: build
	$(DOCKER_RUN) -i --entrypoint /bin/bash -t $(DOCKER_IMAGE)

node_modules: # Build and return node_modules directory using docker
node_modules: build
	mkdir node_modules
	$(DOCKER_RUN) \
		-v $(PWD)/node_modules:/app/node_modules \
		-t $(DOCKER_IMAGE) install

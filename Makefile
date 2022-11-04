USER=$(shell id -u):$(shell id -g)

BACKEND_DIR=backend
FRONTEND_DIR=frontend
MAKE_BACKEND=make --directory=$(BACKEND_DIR)
MAKE_FRONTEND=make --directory=$(FRONTEND_DIR)

all: start

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

dev:		## Start the application in development mode using docker-compose
	docker-compose \
		-f docker-compose.yml \
		-f docker-compose.development.yml \
		up --build --detach

start: 		## Start the application just as in production using docker-compose
	docker-compose up --build --detach

stop:		## Stop the application
	docker-compose down --remove-orphans

clean: 		## Clean the application
clean:
	$(MAKE_BACKEND) clean
	$(MAKE_FRONTEND) clean

lint: 		## Check the format of the whole application
lint:
	$(MAKE_BACKEND) make_lint
	$(MAKE_FRONTEND) lint

format: 	## Reformat the code of the whole application
format:
	$(MAKE_BACKEND) make_format
	$(MAKE_FRONTEND) format

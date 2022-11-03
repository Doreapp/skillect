USER=$(shell id -u):$(shell id -g)

all: start

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

start:		## Start the application using docker-compose
	docker-compose up --build --detach

stop:		## Stop the application
	docker-compose down --remove-orphans

clean: 		## Clean the application
	make --directory=backend clean
	make --directory=frontend clean

USER=$(shell id -u):$(shell id -g)

BACKEND_DIR=backend
FRONTEND_DIR=frontend
MAKE_BACKEND=make --directory=$(BACKEND_DIR)
MAKE_FRONTEND=make --directory=$(FRONTEND_DIR)

DOCKER_USER=antoinemdn
DOCKER_REPO_FRONTEND=skillect-frontend
DOCKER_REPO_BACKEND=skillect-backend
DOCKER_IMAGE_FRONTEND=$(DOCKER_USER)/$(DOCKER_REPO_FRONTEND)
DOCKER_IMAGE_BACKEND=$(DOCKER_USER)/$(DOCKER_REPO_BACKEND)

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

follow: 	## Start following the logs of frontend and backend services
	docker-compose logs --follow backend frontend

push:		## Push docker images to docker hub - Needs DOCKER_PASSWORD environment variable
ifndef DOCKER_PASSWORD
	$(error DOCKER_PASSWORD environment variable has to be set. It is $(DOCKER_USER)'s password)
endif
	@echo Logging in
	@echo "$(DOCKER_PASSWORD)" | docker login --username $(DOCKER_USER) --password-stdin
	@echo Building images
	cd $(FRONTEND_DIR) && docker build -t $(DOCKER_IMAGE_FRONTEND):latest .
	cd $(BACKEND_DIR) && docker build -t $(DOCKER_IMAGE_BACKEND):latest .
	@echo Tagging the images
	$(eval TODAY=$(shell date +%Y-%m-%d-%H-%M)) \
		docker tag $(DOCKER_IMAGE_FRONTEND):latest $(DOCKER_IMAGE_FRONTEND):$(TODAY) \
		&& docker tag $(DOCKER_IMAGE_BACKEND):latest $(DOCKER_IMAGE_BACKEND):$(TODAY)
	@echo Pushing the images
	docker push $(DOCKER_IMAGE_FRONTEND):$(TODAY)
	docker push $(DOCKER_IMAGE_FRONTEND):latest
	docker push $(DOCKER_IMAGE_BACKEND):$(TODAY)
	docker push $(DOCKER_IMAGE_BACKEND):latest
	@echo Docker images are available at:
	@echo "  * https://hub.docker.com/repository/docker/$(DOCKER_IMAGE_FRONTEND)"
	@echo "  * https://hub.docker.com/repository/docker/$(DOCKER_IMAGE_BACKEND)"

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

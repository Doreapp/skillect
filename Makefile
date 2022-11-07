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

SETTINGS_EMAIL=doreapp.contact@gmail.com
TRAEFIK_USERNAME=admin

all: dev

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

production.env: # Create production.env file
ifndef DOMAIN
	$(error DOMAIN variable must be set to server's web domain)
endif
ifndef POSTGRES_USER
	$(error POSTGRES_USER variable must be set to Postgres's username)
endif
ifndef POSTGRES_PASSWORD
	$(error POSTGRES_PASSWORD variable must be set to Postgres's password)
endif
ifndef TRAEFIK_HASHED_PASSWORD
	$(error TRAEFIK_HASHED_PASSWORD variable must be set to Traefik's hashed password)
endif
	@echo "DOMAIN=$(DOMAIN)" >> production.env
	@echo "STACK_NAME=skillect" >> production.env
	@echo "PROJECT_NAME=skillect" >> production.env
	@echo "EMAIL=$(SETTINGS_EMAIL)" >> production.env
	@echo "# Docker images" >> production.env
	@echo "DOCKER_IMAGE_FRONTEND=$(DOCKER_IMAGE_FRONTEND)" >> production.env
	@echo "DOCKER_IMAGE_BACKEND=$(DOCKER_IMAGE_BACKEND)" >> production.env
	@echo "# Traefik variables" >> production.env
	@echo "TRAEFIK_USERNAME=$(TRAEFIK_USERNAME)" >> production.env
	@echo "TRAEFIK_HASHED_PASSWORD=$(TRAEFIK_HASHED_PASSWORD)" >> production.env
	@echo "TRAEFIK_PUBLIC_NETWORK=traefik-public" >> production.env
	@echo "TRAEFIK_TAG=skillect" >> production.env
	@echo "TRAEFIK_PUBLIC_TAG=traefik-public" >> production.env
	@echo "# Postgres variables" >> production.env
	@echo "POSTGRES_SERVER=db" >> production.env
	@echo "POSTGRES_USER=$(POSTGRES_USER)" >> production.env
	@echo "POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)" >> production.env
	@echo "POSTGRES_DB=app" >> production.env
	@echo "# Other variables" >> production.env
	@echo "SENTRY_DSN=" >> production.env
	@echo "SMTP_HOST=" >> production.env

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

pull: 		## Pull the production images from docker hub
pull: production.env
	@echo Pulling the images
	docker-compose --env-file=production.env pull

_deploy_node_update: # For whatever reason, it needs to be extracted to another target
	docker node update \
		--label-add traefik-public.traefik-public-certificates=true \
		$(shell docker info -f '{{.Swarm.NodeID}}')

_deploy_environment: # Create the production environment
	@echo "*** Creating production environment"
	docker swarm init
	docker network create --scope=swarm traefik-public
	make _deploy_node_update

docker-stack.yml: production.env
	docker-compose \
		--env-file=production.env \
		-f docker-compose.yml \
		-f docker-compose.production.yml \
		config >> docker-stack.yml

deploy:		## Start the application just as in production using docker-compose
deploy: stop_deploy _deploy_environment docker-stack.yml
	docker stack deploy -c docker-stack.yml skillect

stop_deploy:	## Stop the deployed application
	docker stack rm skillect || true
	docker network rm traefik-public || true
	docker swarm leave --force || true

stop:		## Stop the application
	docker-compose down --remove-orphans

logs-%:
	docker service logs skillect_$(shell echo $@ | cut -d - -f 2-)

clean: 		## Clean the application
clean:
	$(MAKE_BACKEND) clean
	$(MAKE_FRONTEND) clean
	rm -f production.env docker-stack.yml

lint: 		## Check the format of the whole application
lint:
	$(MAKE_BACKEND) make_lint
	$(MAKE_FRONTEND) lint

format: 	## Reformat the code of the whole application
format:
	$(MAKE_BACKEND) make_format
	$(MAKE_FRONTEND) format

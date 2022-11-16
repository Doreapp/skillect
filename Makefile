USER=$(shell id -u):$(shell id -g)

PROJECT_NAME=skillect

BACKEND_DIR=backend
FRONTEND_DIR=frontend
MAKE_BACKEND=make --directory=$(BACKEND_DIR)
MAKE_FRONTEND=make --directory=$(FRONTEND_DIR)

DOCKER_USER=antoinemdn
DOCKER_REPO_FRONTEND=$(PROJECT_NAME)-frontend
DOCKER_REPO_BACKEND=$(PROJECT_NAME)-backend
DOCKER_IMAGE_FRONTEND=$(DOCKER_USER)/$(DOCKER_REPO_FRONTEND)
DOCKER_IMAGE_BACKEND=$(DOCKER_USER)/$(DOCKER_REPO_BACKEND)

DOCKER_COMPOSE_DEVELOPMENT=docker-compose -f docker-compose.yml -f docker-compose.development.yml
DOCKER_COMPOSE_PRODUCTION=docker-compose -f docker-compose.yml -f docker-compose.production.yml

TRAEFIK_PUBLIC_NETWORK=traefik-public
DOMAIN=mandin.dev

SSH_USER=deployer
DEPLOYEMENT_REF=main

all: up

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

.env.dev: # Generate development .env
	@cp env/base.env .env
	@echo "" >> .env
	@cat env/development.env >> .env

.env.prod: # Generate production .env
ifndef POSTGRES_PASSWORD
	$(error POSTGRES_PASSWORD environment variable not set)
endif
	@cp env/base.env .env
	@echo "" >> .env
	@echo "# Production environment variables" >> .env
	@echo "DOMAIN=${DOMAIN}" >> .env
	@echo "DOCKER_IMAGE_BACKEND=${DOCKER_IMAGE_BACKEND}" >> .env
	@echo "DOCKER_IMAGE_FRONTEND=${DOCKER_IMAGE_FRONTEND}" >> .env
	@echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> .env


dev:		## Start the application in development mode using docker-compose
dev: .env.dev
	$(DOCKER_COMPOSE_DEVELOPMENT) \
		up --build --detach

$(TRAEFIK_PUBLIC_NETWORK): # Create the network
	@docker network create $(TRAEFIK_PUBLIC_NETWORK) || \
		echo "> $(TRAEFIK_PUBLIC_NETWORK) network already exist."

deploy: 	## Start the app in production mode
deploy: .env.prod $(TRAEFIK_PUBLIC_NETWORK) stop
	$(DOCKER_COMPOSE_PRODUCTION) pull
	$(DOCKER_COMPOSE_PRODUCTION) up --detach

known_hosts:
	ssh-keyscan -H $(DOMAIN) > known_hosts

ssh_key: # Note: SSH_KEY must be the rsa ssh key with new lines (\n) replaced by #
ifndef SSH_KEY
	$(error SSH_KEY must be defined. It is the private key to use in order to login via SSH)
endif
	touch ssh_key
	chmod 600 ssh_key
	echo "$(SSH_KEY)" | sed -r 's/#/\n/g' >> ssh_key
	chmod 400 ssh_key

ssh_deploy:	## Connect via SSH to the deployment device and deploy the latest version of the app
ssh_deploy: known_hosts ssh_key
	ssh -o UserKnownHostsFile=known_hosts \
		-i ssh_key \
		$(SSH_USER)@$(DOMAIN) \
			"cd /home/${SSH_USER}/$(PROJECT_NAME) \
			&& git fetch -p \
			&& git reset --hard origin/$(DEPLOYEMENT_REF) \
			&& make deploy \
				POSTGRES_PASSWORD=$(POSTGRES_PASSWORD)"

follow: 	## Start following the logs of frontend and backend services
	docker-compose logs --follow backend frontend

push:		## Push docker images to docker hub - Needs DOCKER_PASSWORD environment variable
ifndef DOCKER_PASSWORD
	$(error DOCKER_PASSWORD environment variable has to be set. It is $(DOCKER_USER)'s password)
endif
	@echo Logging in
	@echo "$(DOCKER_PASSWORD)" | docker login --username $(DOCKER_USER) --password-stdin
	@echo Building images
	cd $(FRONTEND_DIR) && docker build \
		--build-arg URL=https://${DOMAIN} -t $(DOCKER_IMAGE_FRONTEND):latest .
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

PYTHON=python3

APP_DIR=app/
GUNICORN_CONF=gunicorn_conf.py

DOCKER_IMAGE=skillect-backend
CELERY_DOCKER_IMAGE=skillect-celery-worker
DOCKER_RUN=docker run \
 -u $(shell id -u):$(shell id -g) \
 -v $(shell pwd)/$(APP_DIR):/work/$(APP_DIR)

LINE_LENGTH=100

all: build make_lint

help: 		## Display help message
help:
	@echo Make targets:
	@echo
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

build: 		## Build docker image
	docker build -t $(DOCKER_IMAGE) .

make_%: 	## Run 'make %' inside docker image
make_%: build
	$(DOCKER_RUN) $(OPTIONS) \
		-t $(DOCKER_IMAGE) \
		$(shell echo $@ | cut -c 6-)

clean: 		## Clean the directory
	@rm -rf *.dist-info *.egg-info *.whl
	@rm -rf build logs .pytest_cache
	@find . -type d -name __pycache__ -exec rm -rf {} \; || true
	@find . -type f -name "*.pyc" -exec rm -rf {} \; || true
	@find . -type f -name "*.pyo" -exec rm -rf {} \; || true

format: 	## Run isort and black to reformat code
	@${PYTHON} -m isort --line-length ${LINE_LENGTH} --profile black ${APP_DIR}
	@${PYTHON} -m black --line-length ${LINE_LENGTH} ${APP_DIR}

lint: 		## Check code with isort, black and pylint
	${PYTHON} -m isort --line-length ${LINE_LENGTH} --profile black --check ${APP_DIR}
	${PYTHON} -m black --line-length ${LINE_LENGTH} --check ${APP_DIR}
	${PYTHON} -m pylint --load-plugins pylint_pytest ${APP_DIR}

_interactive: # Enter the docker container in interactive mode
_interactive: build
	$(DOCKER_RUN) --entrypoint /bin/bash -i $(OPTIONS) -t $(DOCKER_IMAGE)

_wait_for_db: # Call python script to wait for the database to be up
	${PYTHON} -m app.wait_for_db

_init: # Initialize the database
_init: _wait_for_db
	${PYTHON} -m app.initial_data

dev: # Start the backend server in development mode
dev: _init
	uvicorn \
		--reload \
		--host 0.0.0.0 \
		--port 5000 \
		--log-level info \
		"app.main:app"

serve: # Start the backend server in production mode
serve: _init
	gunicorn -k uvicorn.workers.UvicornWorker -c "${GUNICORN_CONF}" "app.main:app"

start_worker: # Start the celery worker
start_worker: _wait_for_db
	celery -A app.worker worker -l info -Q main-queue -c 1

# Skillect backend

Python-based web server, storing and serving models for the frontend.

## How to use

The server must be used along with a database, a Message Queue broker and workers. Thus, to run it (even in development mode), one must use `docker-compose`. Additional information are available in [global README](../README.md).

## Engine

The web server is based on:
- [FastAPI](https://fastapi.tiangolo.com/) for the REST web server
- [gunicorn](https://gunicorn.org/) for the WSGI HTTP Server
- [PostgreSQL](https://www.postgresql.org/) for the database storage, coupled with [SQLAlchemy](https://sqlalchemy.org/) on python's side
- [Celery](https://docs.celeryq.dev/en/stable/index.html) workers with [RabbitMQ](https://www.rabbitmq.com/) message broker

## Contents

This directory contains the configurations and scripts of the backend.

| File(s) | Description |
| --- | --- |
| [`requirements.txt`](requirements.txt) | `pip` requirements for the server |
| [`requirements-dev.txt`](requirements-dev.txt) | `pip` requirements during development |
| [`Makefile.txt`](Makefile) | Contains development scripts |
| [`gunicorn_conf.py`](gunicorn_conf.py) | Configuration of `gunicorn` production server |
| [`Dockerfile`](Dockerfile) | Dockerfile describing docker images of the server and the celery worker |
| [`.pylintrc`](pylintrc) | Configuration of `pylint` |
| [`app`](app) | Source-code directory containing the **magic** |

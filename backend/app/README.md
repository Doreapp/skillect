# Backend source code

This directory is a python module having several entrypoints.

- [`main.py`](main.py) - Main script. Creates the `app` object served by `gunicorn`.
- [`wait_for_db.py`](wait_for_db.py) - Script waiting up to 5 minutes for the database to come online.
- [`initial_data.py`](initial_data.py) - Script initializing the database.
- [`worker.py`](worker.py) - Script used by celery workers.

## Modules

| Name | Description |
| --- | --- |
| [`api`](api) | REST API description and behavior |
| [`core`](core) | Main scripts |
| [`crud`](crud) | Create/Read/Update/Delete facilities |
| [`db`](db) | Database connections |
| [`models`](models) | Description of the models manipulated |
| [`schemas`](schemas) | Database schemas |

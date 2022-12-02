Architecture
============

Overall architecture
--------------------

**Skillect** webiste uses a client-server architecture.

The :ref:`backend <ref-backend>` serves a secured
`REST <https://en.wikipedia.org/wiki/Representational_state_transfer>`_ API used by the
:ref:`frontend <ref-frontend>`.

Both services are under a reverse proxy based on `Traefik <https://traefik.io/>`_.
It defines the domain name of the website (which is ``mandin.dev`` here)
and enables `HTTPS <https://en.wikipedia.org/wiki/HTTPS>`_ using `Let's Encrypt <https://letsencrypt.org/>`_ certificate authority.

Each service is in a `Docker <https://www.docker.com/>`_ container.
The overall network is described in a `docker compose <https://docs.docker.com/compose/>`_ configuration.

The overall architecture can be represented as:



.. _ref-backend:

Backend
-------

The backend is made of a python server (based on `FastAPI <https://fastapi.tiangolo.com/>`_).
It uses an SQL database using `PostgreSQL` technology.

The backend serves a `REST` API using `gunicorn` server.

The main language used is `python`.

.. warning ::
    PostgreSQL link
    REST link


.. _ref-frontend:

Frontend
--------

.. warning ::
    TODO React, MUI, Tailwind, Ngnix

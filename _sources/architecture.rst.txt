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

.. _ref-backend:

Backend
-------

.. warning ::
    TODO Python, fastapi, gunicorn, REST...


.. _ref-frontend:

Frontend
--------

.. warning ::
    TODO React, MUI, Tailwind, Ngnix

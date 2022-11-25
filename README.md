# <img src="frontend/public/logo512.png" alt="logo" width="48"/> Skillect

A Client-Server website, meant to store and display experiences and skills.

**🎉🌐 Website:** [`https://mandin.dev`](https://mandin.dev).

**📝 Documentation:** [`https://doreapp.github.io/skillect`](https://doreapp.github.io/skillect/)

> 💡 Inspired from [full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql) project.

## How to use

One need `docker` and `docker-compose` to start the application.

Run `make`.

Then open [`http://localhost`](http://localhost).

You can also access webpages of [Swagger](http://localhost/docs) and [ReDoc](http://localhost/redoc)

## Deployment

Deployment considers that you have a remote device, in which you can connect via SSH.

### Manual deploy

1. Connect in ssh to the device
2. Clone the project: `git clone https://github.com/Doreapp/skillect.git`.

    And enter in project's directory: `cd skillect`
3. Deploy the website: `make deploy`. You need to define several environment variables, described [here](#environment-variables)

### Continuous Deployment

GitHub actions are setup to deploy the project automatically, each time a change is pushed to `main` branch.

For the *CD* to run as intended, you need to define some *Actions secrets* in GitHub repository's settings. First, there are all the environment variables described [here](#environment-variables) (that can also be set directly in the `Makefile`) but also:
- `FIRST_SUPERUSER`, email address identifying the initial superuser
- `FIRST_SUPERUSER_PASSWORD`, password of the first superuser
- `POSTGRES_PASSWORD`, password to connect to *Postgres* database
- `SSH_KEY`, RSA ssh key to connect to the deployment target, **With new lines (`\n`) replaced by `#`)**

### Environment variables

Default values for environment variables are defined in [`base.env`](env/base.env) and [`development.env`](env/development.env) files.

Other environment variables are defined on top of the [`Makefile`](Makefile), such as:
- `TRAEFIK_PUBLIC_NETWORK`, it can remain to default.
- `DOMAIN`, it is your domain name (like `www.google.com`).
- `SSH_USER`, it is the user to use during ssh communication with deployment target.

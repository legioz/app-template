# Web App Template │ Structure
Web app template for python frameworks(FastAPI, Flask, Bottle...)

## Requirements
* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Node.js](https://nodejs.org/en/) (with `npm`).

## Backend local development

* Start the stack with Docker Compose:

```bash
docker-compose build
docker-compose up -d
```

* Now you can open your browser and interact with these URLs:

Frontend, built with Docker, with routes handled based on the path: http://localhost

Backend, JSON based web API based on OpenAPI: http://localhost/api/

Automatic interactive documentation with Swagger UI (from the OpenAPI backend): http://localhost/docs

Alternative automatic documentation with ReDoc (from the OpenAPI backend): http://localhost/redoc

**Note**: The first time you start your stack, it might take a minute for it to be ready. While the backend waits for the database to be ready and configures everything. You can check the logs to monitor it.

To check the logs, run:

```bash
docker-compose logs
```

To check the logs of a specific service, add the name of the service, e.g.:

```bash
docker-compose logs backend
```

### .env file:

The `.env` file is the one that contains all your configurations, generated keys and passwords, etc.

Depending on your workflow, you could want to exclude it from Git, for example if your project is public. In that case, you would have to make sure to set up a way for your CI tools to obtain it while building or deploying your project.

One way to do it could be to add each environment variable to your CI/CD system, and updating the `docker-compose.yml` file to read that specific env var instead of reading the `.env` file.

```sh
DEBUG=True
PROJECT_NAME=''
SECRET_KEY=''

MARIADB_USER='us3r'
MARIADB_PASS='123456'
MARIADB_HOST='db'
MARIADB_DB='db'

SMTP_HOST=''
SMTP_USER=''
SMTP_PASSWORD=''
SMTP_EMAIL=''
SMTP_TLS=True
SMTP_PORT=587

SENTRY_DSN=

VUE_APP_DOMAIN_DEV=localhost
VUE_APP_DOMAIN_STAG=stag.projeto1teste.com
VUE_APP_DOMAIN_PROD=projeto1teste.com
VUE_APP_NAME=Teste
VUE_APP_ENV=development

```

### Default directory tree:
```
── app
    ├── database
    ├── redis
    ├── job
    ├── logs
    ├── mail
    ├── src
    │    ├── api
    │    │   ├── router.py
    │    │   └── routes
    │    │       ├── auth_v1.py
    │    │       ├── auth_v2.py
    │    │       └── hello_world.py
    │    │        
    │    ├── certificates
    │    │   └── docker_CA.crt
    │    ├── core
    │    │   ├── config.py
    │    │   ├── schema
    │    │   │   └── database.sql
    │    │   └── security.py
    │    ├── docker-compose.yml
    │    ├── Dockerfile
    │    ├── main.py
    │    ├── README.md
    │    ├── static
    │    │   └── style.css
    │    └── templates
    │        ├── auth
    │        │   └── login.html
    │        ├── base.html
    │        └── hello_world
    │            └── hello_world.html
    │    
    └── upload
```

### Development URLs

Development URLs, for local development.

Frontend: http://localhost

Backend: http://localhost/api/

Automatic Interactive Docs (Swagger UI): https://localhost/docs

Automatic Alternative Docs (ReDoc): https://localhost/redoc


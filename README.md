# Web App Template │ Structure
Web app template for python frameworks(FastAPI, Flask, Bottle...)

## Requirements
* [Docker](https://www.docker.com/).
* [Docker Compose](https://docs.docker.com/compose/install/).
* [Node.js](https://nodejs.org/en/) (with `npm`).

## Backend local development


* First Time Build:
```bash
cd scripts/
./first-build.sh
```

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
OPENAPI_URL=/openapi.json
DOCS_URL=/docs
REDOCS_URL=/redoc
PROJECT_NAME=
SECRET_KEY=

MARIADB_USER='us3r'
MARIADB_PASS='123456'
MARIADB_HOST='db'
MARIADB_DB='db'

SMTP_HOST=
SMTP_USER=
SMTP_PASSWORD=
SMTP_EMAIL=
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
app
├── backend('src')
│   ├── api
│   │   ├── router.py
│   │   └── routes
│   │       ├── auth_v1.py
│   ├── app
│   │   ├── router.py
│   │   └── routes
│   │       └── main.py
│   ├── certificates
│   │   └── docker_CA.crt
│   ├── core
│   │   ├── config.py
│   │   ├── databases.py
│   │   ├── schema
│   │   │   ├── json
│   │   │   │   └── countries-states-cities.json
│   │   │   └── sql
│   │   │       └── database.sql
│   │   └── security.py
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   ├── static
│   │   ├── css
│   │   │   └── style.css
│   │   └── mobile
│   │       └── manifest.json
│   └── templates
│
│
│
├── frontend
│   ├── babel.config.js
│   ├── Dockerfile
│   ├── nginx-backend-not-found.conf
│   ├── nginx.conf
│   ├── package.json
│   ├── public
│   │   ├── favicon.ico
│   │   ├── img
│   │   │   └── icons
│   │   ├── index.html
│   │   ├── manifest.json
│   │   └── robots.txt
│   ├── README.md
│   ├── src
│   │   ├── App.vue
│   │   ├── assets
│   │   │   └── logo.png
│   │   ├── components
│   │   │   └── HelloWorld.vue
│   │   ├── config.js
│   │   └── main.js
│   └── tests
│       └── unit
│           └── upload-button.spec.ts
│
│
├── docker-compose.yml
├── README.md
└── scripts
    └── first-build.sh
```

### Development URLs

Development URLs, for local development.

Frontend: http://localhost

Backend: http://localhost/api/

Automatic Interactive Docs (Swagger UI): https://localhost/docs

Automatic Alternative Docs (ReDoc): https://localhost/redoc


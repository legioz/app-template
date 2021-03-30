# Web App Template │ Structure
Web app template for python frameworks(FastAPI, Flask, Bottle...)

### Usage:
```sh
run.sh
```
### .env:
```sh
PROJECT_NAME=''
SECRET_KEY=''
DEBUG=True
MARIADB_USER='us3r'
MARIADB_PASS='123456'
MARIADB_HOST='mariadb'
MARIADB_DB='db'
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

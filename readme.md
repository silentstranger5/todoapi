# TODO API

This is a To-Do List API

## App Stack

| Name | Role |
|------|------|
| Python| Runtime Environment |
| Postgres | Database |
| FastAPI  | API Framework |
| SQLAlchemy | SQL Toolkit & ORM |
| Pytest | Testing Environment |

## Requirements

- Python 3.10+ [Website](https://python.org)
- Postgres [Website](https://www.postgresql.org)

## How to install

Before you start an application, configure your database server parameters via `todo/config.py`.
Application requires configuration of a database specified in config.py. By default, it's called `postgres`.

```
git clone https://github.com/silentstranger5/todoapi.git
cd todoapi
# configure your virtual environment (optionally)
python -m venv .venv
.venv/bin/activate
# install dependencies
pip install -e .
# edit config.py and replace values with appropriate ones
editor todo/config.py
# finally, startup an app
fastapi dev todo/main.py
```

## How to test

Testing requires configuration of an additioinal database. By default, it's called `test`.

```
pytest
```

## How to send requests

After you launched an application, it should be available at [http://localhost:8000/](http://localhost:8000/).
You can find documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
In order to send a request with data, you need to set up header `Content-Type: application/json`
and send your data via a POST request.
To authenticate, you need to register as a user and then get your access token.
After that, you need to set up header `Authorization: Bearer TOKEN`. Replace `TOKEN` with your 
authorization token.
You can try to send requests with `curl` utility.
You can also use documentation to send requests as well.

Here is how you can register:

```
curl --request POST \
    --header "Content-Type: application/json" \
    --data '{"username": "user", "password": "password"}' \
    http://localhost:8000/auth/register

# {"message": "Registration is successful"}
```

Get your authentication token:

```
curl --request POST \
    --header "Content-Type: application/json" \
    --data '{"username": "user", "password": "password"}' \
    http://localhost:8000/auth/token

# {"access_token": "asdfiu0983jfoaiwhoq43ih.qfo98h4wfiuhq4of87houfao9834fh.OIUH087h3hfoijhOIH76034...", "token_type": "bearer"}
```

Get your tasks:

```
curl \
    --header "Authorization: Bearer asdfiu0983jfoaiwhoq43ih.qfo98h4wfiuhq4of87houfao9834fh.OIUH087h3hfoijhOIH..." \
    http://localhost:8000/tasks/get

# {"tasks": []}
```

Create a new task:

```
curl --request POST \
    --header "Authorization: Bearer asdfiu0983jfoaiwhoq43ih.qfo98h4wfiuhq4of87houfao9834fh.OIUH087h3hfoijhOIH..." \
    --header "Content-Type: application/json" \
    --data '{"name": "Write a new app"} \
    http://localhost:8000/tasks/create

# {"message": "Task successfully created"}
```

## Modules

| Name | Description |
|------|-------------|
| auth.py | Registration and authentication via JWT tokens |
| config.py   | Configuration details  |
| crud.py  | Database CRUD operations  |
| database.py | Database configuration |
| main.py | Application entry point |
| models.py   | SQLAlchemy Data Models |
| permissions.py | Grant read and update permissions to other users |
| schemas.py  | Pydantic Models used for input |
| tasks.py | Create, read, update and delete tasks |
| tests/   | Test Directory |

# Task Management API

This is a CRUD API for Task Management with Undo function

## Requirements
Install:
- Python 3.10 or higher (https://www.python.org/downloads/release/python-3100/)
- Poetry (https://python-poetry.org/docs/)
- Docker (https://www.docker.com/)

## How to Run

1. Install `Python 3.10` `Poetry` `Docker`
2. Clone this Repo

3. Navigate to inside the project's `/app` folder

4. Run ```poetry install``` in terminal

5. Set up docker for postgres by runing this command in the terminal:
```bash
docker run --rm --name postgres -p 5555:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -d postgres:14
```

6. Check if postgres is running properly in docker: 
```bash
docker exec -it postgres psql -U postgres
```
7. Run data migration for postgres using alembic via poetry: 
```bash
poetry run alembic init -t async migrations

poetry run alembic revision --autogenerate -m 'adds task and task_history table'

poetry run alembic upgrade head
```
8. Run server by running this command in terminal:
```bash
poetry run uvicorn main:app --reload
```

9. Swagger is available:
```url
http://127.0.0.1:8000/docs
```
For More Detail, please refer to this APIdocs:
```
https://illustrious-cheque-071.notion.site/API-Reference-bec1b71e41df4c3b8a57d3f34996e2f7?pvs=4
```



## Usage

I would have write a data populate script, but with the current state, it would require you to create new tasks several time via CREATE endpoint. After several Tasks are created, we can use other endpoints to interact.



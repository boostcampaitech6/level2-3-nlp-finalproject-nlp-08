## How to run server (with docker compose)
```
cd backend
docker-compose up -d
```

## How to run locally

1. Install Postgresql Database(for mac) `brew install postgresql@14`
2. start database server `brew services start postgresql`
3. access psql shell `psql postgres`
4. show databses `postgres=# \l`
5. create databse (ex.testdb) `CREATE DATABASE testdb;`
6. show databses `postgres=# \l`
7. replace databse uri `postgresql://<username>@localhost:5432/<testdb>` on config.yaml
4. Install poetry : https://python-poetry.org/docs/
5. poetry shell
6. poetry install 
7. python src/main.py

## PostgreSQL commands
stop postgresql server `brew services stop postgresql`

change database `postgres=# \c testdb`

show tables `postgres=# \dt`

show rows from table `SELECT * FROM userfeedbacks;`
## API docs
localhost:8000/docs

localhost:8000/redoc
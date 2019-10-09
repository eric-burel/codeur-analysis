## Run

Run a docker instance of the database.
DB is available on `localhost:5432`. (default access: "postgres" and "admin123")
Adminer UI is available on `localhost:8080`

```
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up
```

You need to install a Postgre client on your machine.

For Ubuntu:

```
sudo apt-get install libpq-dev # for psycopg internally
sudo apt install postgresql-client-common # to run restore
sudo apt-get install postgresql-client
```

## Python virutal env

`source ./venv/bin/activate`

## Python version

3.6.9

## TODO

- [ ] Run a postgre db
- [ ] Connect to the db
- [ ] Send backups to the db
- [ ] Create a Jupyter lab to visualize missions using Bokeh
- [ ] Run scripts with nltk

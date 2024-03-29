## Install

### Python

```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements
# if you encounter issues with pkg-ressources, just remove it from the requirements.txt
```

### Database

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

### Load dumps

Dumps should be stored in the `./dumps` folder (at the root or nested).

```
PGPASSWORD="admin123" ./load_backup.py
```

### Use Jupyter

You need to create a Kernel for the local virtual env.
https://janakiev.com/blog/jupyter-virtual-envs/

```
python -m pip install --user ipykernel
python -m ipykernel install --user --name=myenv
```

### Use Dash

```
python dash/dev_server.py
```

The Dash Standard Button is provided by https://github.com/lbke/dash-standard-button (see Readme for build instruction). The built tarball can be unzipped and added in the "Dash" folder.

## Python version

3.6.9

## Access data through Mode Analytics

Use a [Bridge Connector](https://mode.com/help/articles/how-mode-connects/#run-bridge-in-a-docker-container) to connect to the local database.

Run it in Docker.

```
docker start mode-bridge
```

## Heroku deployment

Please check that `requirements.txt` is correctly set in the `dash` folder.

Push the subfolder:

```
    git subtree push --prefix dash heroku master
```

## TODO

- [x] Run a postgre db
- [x] Connect to the db
- [x] Send backups to the db
- [x] Actually handle multiple restore (right now pg_restore produce errors)
- [x] Include a Dash dashboard
- [ ] Fix dup deletion => will remove ALL copies
- [ ] Create a Jupyter lab to visualize missions using Bokeh
- [ ] Run scripts with nltk to analyze text
- [ ] Automate dump loading
- [ ] Improve scraper to get more infos

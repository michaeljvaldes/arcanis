install: # install the server dependencies
    pip install -r requirements.txt

server_start: # start the django server
    python3 manage.py runserver

db_start: # start the database docker container
    docker run arcanis_db

db_stop: # stop the database docker container
    docker stop arcanis_db

db_create: # create the database docker container
    docker-compose --env-file ./env/dev.env up -d db

db_destroy: # destroy the database docker container and volume
    if docker ps -a | grep arcanis_db; then docker-compose rm -s -f -v db; fi
    if docker volume ls | grep arcanis_db_vol; then docker volume rm arcanis_db_vol; fi

makemigrations: # generate migrations based on models
    python3 manage.py makemigrations playgroups

migrate: # apply migrations to the database
    python3 manage.py migrate

loaddata: # load test data from fixtures into the database
    python3 manage.py loaddata some_users commanders squirrels

db_reset: # destroy, recreate, and reseed test data into the database
    just db_destroy
    just db_create
    sleep 1
    just migrate
    just loaddata

document: # generate api documentation
    python3 manage.py spectacular --color --file schema.yml

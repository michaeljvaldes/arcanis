### server ###

install: # install the server dependencies
    pip install -r app/requirements.txt

server_start: # start the django server
    python3 app/manage.py runserver


### database ###

db_start: # start the database docker container
    docker run arcanis-db

db_stop: # stop the database docker container
    docker stop arcanis-db

db_create: # create the database docker container
    docker-compose up -d db

db_destroy: # destroy the database docker container and volume
    if docker ps -a | grep arcanis-db; then docker-compose rm -s -f -v db; fi
    if docker volume ls | grep arcanis_db_vol; then docker volume rm arcanis_db_vol; fi

makemigrations: # generate migrations based on models
    python3 app/manage.py makemigrations playgroups

migrate: # apply migrations to the database
    python3 app/manage.py migrate

loaddata: # load test data from fixtures into the database
    python3 app/manage.py loaddata some_users commanders squirrels

db_reset: # destroy, recreate, and reseed test data into the database
    just db_destroy
    just db_create
    sleep 1
    just migrate
    just loaddata


### other ###

document: # generate api documentation
    python3 app/manage.py spectacular --color --file schema.yml

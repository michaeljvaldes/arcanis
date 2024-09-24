### server ###

install: # install server dependencies
    pip install -r app/requirements.txt

server_start: # start django server
    python3 app/manage.py runserver


### server (docker) ###

server_create: # create and run server docker container
    docker-compose -f docker-compose.dev.yml up -d web

server_destroy: # destroy server docker container
    if docker ps -a | grep arcanis-server; \
        then docker-compose -f docker-compose.dev.yml rm -s -f -v web; \
        else echo "no server containers found"; \
    fi

server_reset: # destroy and recreate server container
    just server_destroy
    just server_create

### database ###
db_stop: # stop database docker container
    docker stop arcanis-db

db_create: # create and run database docker container
    docker-compose -f docker-compose.dev.yml up -d db

db_destroy: # destroy database docker container and volume
    if docker ps -a | grep arcanis-db; \
        then docker-compose rm -s -f -v db; \
        else echo "No database containers found"; \
    fi
    if docker volume ls | grep arcanis-db_vol; \
        then docker volume rm arcanis_db_vol; \
        else echo "No database volumes found"; \
    fi

makemigrations: # generate migrations based on models
    python3 app/manage.py makemigrations playgroups

migrate: # apply migrations to database
    python3 app/manage.py migrate

migrate_docker: # apply migrations from server docker container
    if ! docker ps | grep arcanis-db; \
        then echo "database container must be running"; \
    fi 
    if docker ps | grep arcanis-server; \
        then docker-compose -f docker-compose.dev.yml exec web python manage.py migrate; \
        else echo "server container must be running"; \
    fi

loaddata: # load test data from fixtures into database
    python3 app/manage.py loaddata some_users commanders squirrels

loaddata_docker: # load test data from fixtures into database from server docker container
    if ! docker ps | grep arcanis-db; \
        then echo "database container must be running"; \
    fi 
    if docker ps | grep arcanis-server; \
        then docker-compose -f docker-compose.dev.yml exec web python manage.py loaddata some_users commanders squirrels; \
        else echo "server container must be running"; \
    fi

db_reset: # destroy, recreate, and reseed test data into database
    just db_destroy
    just db_create
    sleep 1
    just migrate
    just loaddata

db_reset_docker: # destroy, recreate, and reseed test data into database from within server container
    just db_destroy
    just db_create
    sleep 1
    just migrate_docker
    just loaddata_docker

### other ###

build_fresh: # destroy, create, and run server and database containers with test data
    just server_reset
    just db_reset_docker

document: # generate api documentation
    python3 app/manage.py spectacular --color --file schema.yml

install:
    pip install -r requirements/dev.txt

run: 
    python3 manage.py runserver

run_docker: 
    docker-compose --env-file env/docker.env up -d

makemigrations: 
    python3 manage.py makemigrations playgroups

migrate: 
    python3 manage.py migrate

loaddata: 
    python3 manage.py loaddata some_users commanders matches

db_flush: 
    python3 manage.py flush

db_reset: 
    db_flush makemigrations migrate loaddata

document:
    python3 manage.py spectacular --color --file schema.yml
run: python3 manage.py runserver

run docker: docker-compose --env-file env/docker.env up -d

makemigrations: python3 manage.py makemigrations playgroups

migrate: python3 manage.py migrate

loaddata: python3 manage.py loaddata some_users commanders matches

flush_db: python3 manage.py flush

reset_db: flush_db makemigrations migrate loaddata

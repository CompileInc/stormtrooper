# Installation

## Docker

install docker

    pip install docker-compose
    docker-compose up
    docker exec stormtrooper_db_1 createdb -Upostgres stormtrooper

If you're using OSX, app would be hosted on the docker-machine's IP.
You can find it out by doing

    docker-machine ip MACHINE_NAME

`MACHINE_NAME` is usually `default`

## Database (postgres 9.4)

    CREATE DATABASE stormtrooper;
    CREATE ROLE trooper PASSWORD 'trooper' LOGIN;
    GRANT ALL PRIVILEGES ON DATABASE stormtrooper TO trooper;

## Python

    pip install -r requirements.txt
    pip install -r requirements-dev.txt # development
    cd stormtrooper
    python manage.py migrate
    python manage.py seed tasker --number=15 # development
    python manage.py bower install
    python manage.py createsuperuser



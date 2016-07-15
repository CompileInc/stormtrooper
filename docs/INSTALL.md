# Installation

## Requirements
- Python 2.7
- Postgres 9.4+
- Redis

## Database (postgres 9.4+)

    CREATE DATABASE stormtrooper;
    CREATE ROLE trooper PASSWORD 'trooper' LOGIN;
    GRANT ALL PRIVILEGES ON DATABASE stormtrooper TO trooper;

## Python

    pip install -r requirements.txt
    pip install -r requirements-dev.txt # development
    cd stormtrooper
    cp stormtrooper/localsettings.py.sample stormtrooper/localsettings.py   # Change your values appropriately
    python manage.py migrate
    python manage.py createsuperuser

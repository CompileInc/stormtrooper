# Installation

    pip install -r requirements.txt
    pip install -r requirements-dev.txt # development
    cd stormtrooper
    python manage.py migrate
    python manage.py seed tasker --number=15 # development
    python manage.py bower install
    python manage.py createsuperuser

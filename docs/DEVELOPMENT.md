## Docker

- Append ```localsettings.py``` with docker-specific settings (```docker-settings.py.sample```). ```cat stormtrooper/docker-settings.py >> stormtrooper/localsettings.py```
- Install docker
- ```pip install docker-compose```
- ```docker-compose up --build```
- ```docker exec stormtrooper_db_1 createdb -Upostgres stormtrooper```
- <kbd>Ctrl</kdb> + <kbd>C</kbd> and restart again with ```docker-compose up```

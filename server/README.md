# Smart Campus Server

## Install
+ gedit config.py
+ python migrate.py db init
+ python migrate.py db migrate
+ python migrate.py db upgrade

## Running
> Nginx + Gunicorn/Supervisor + Flask-RESTful
>
> /usr/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

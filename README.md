## Introduction

We see it all of the time on the big screen - a loved one is lost and the living can't
help but fret that they never 'told them I loved them.'  We can't help it when we
ask ourselves 'When was the last time I told my significant other I loved them?'
Worry no more!  ILU is a service for sending and tracking that special message
to the person we care about most.

Base template for creating flask app - borrowed heavily from [flask recipe](https://gitlab.com/patkennedy79/flask_recipe_app)

## How to Run (Development)

With docker, etting started is as easy as `make init_project`.  This
handles:
1. Creating the Dockerfile for the postgres service. The db 
configuraitons in web/instance/flask.cfg are copied to postgresql/Dockerfile
1. Building the docker images
1. Starting the docker containers
1. Initializing the database

Go to your favorite web browser and open:
    http://localhost:5000  $ Or check the IP address using 'docker-machine ip'

## How to Run (Production)

The production environment can be started with `make prod`

The production environment uses gunicorn and nginx containers. By
specifying 'docker-compose.yml' in the make command, docker does
not run docker-compose.override.yml, which is run by default

## Key Python Modules Used

- Flask - web framework
- SQLAlchemy - ORM (Object Relational Mapper)
- Flask-Login - support for user management
- Flask-Migrate - database migrations
- Flask-WTF - simplifies forms

This application is written using Python 3.6.3.  The database used is PostgreSQL.

## Unit Testing

In the top-level folder:
    % nose2

For running a specific module:
    % nose2 -v project.tests.test_module.py

## TODO

There's loads of room for improvement:

1. Get `make test` working
1. Create API documentation
1. Document classes and functions
1. Separate local requirements from production
1. Use class based views
1. Reorganize config files to 'local', 'dev', 'staging', 'production'
1. Use token based authentication

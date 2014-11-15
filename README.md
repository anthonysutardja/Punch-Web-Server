# Punch Web Repository
This repository contains the application code to run the Punch web server. The Punch web server acts
as the main portal for users to access their sensor data and manage notification settings.

## Requirements
Postgresql installed. Check out [Postgres.app](http://postgresapp.com/) to run a standalone installation
of the Postgresql SQL Server.

## Installation
Download the repository and change into the top level directory.

Run the following in your shell:

    ./bootstrap.sh

This will install all the necessary Python requirements and setup the punch database user and database.

## Running the server

    python manage.py runserver

## Running tests

    python manage.py test

## Running migrations and upgrading the database

    python manage.py migrate

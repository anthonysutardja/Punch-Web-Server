#!/bin/sh

# Clear all cache
find . -name '*.pyc' -delete;

# Create a new database user called punch with no password (if it doesn't exist)
psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='punch'" | grep -q 1 || createuser punch -d;
# Create a new database and set the owner to the punch user (if it doesn't exist)
psql -l | grep -q punch_db && dropdb punch_db;
psql -l | grep -q punch_db || createdb punch_db -O punch;

# Run migrations
python manage.py migrate;

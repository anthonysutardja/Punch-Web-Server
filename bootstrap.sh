#!/bin/sh

# Install python requirements
pip install -r requirements.txt;
pip install -r requirements-dev.txt;
# Create a new database user called punch with no password (if it doesn't exist)
psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='punch'" | grep -q 1 || createuser punch -d;
# Create a new database and set the owner to the punch user (if it doesn't exist)
psql -l | grep -q punch_db || createdb punch_db -O punch;
psql -l | grep -q test_punch_db || test_createdb punch_db -O punch;
# Run migrations
python manage.py migrate;

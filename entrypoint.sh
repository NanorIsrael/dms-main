#!/bin/sh
echo "Waiting for database to be ready..."
while ! nc -z db_main 5432; do
  sleep 1
done
echo "Database is ready!"
flask --app main db upgrade
exec python3 main.py

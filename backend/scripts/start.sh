#!/bin/bash

# Run Alembic migrations
# Need to be in the directory where alembic.ini is, or specify its path
echo "Running database migrations..."
alembic upgrade head

# Start Uvicorn server
echo "Starting Uvicorn server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

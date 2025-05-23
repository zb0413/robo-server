# Use an official Python runtime as a parent image
FROM python:3.9-slim

RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/

# Set the working directory in the container
WORKDIR /app

# Install system dependencies that might be needed by Python packages
# For example, ffmpeg itself if it's not expected to be on the host or in another container
# For now, we assume ffmpeg is handled separately (e.g., host or another container in Docker Compose)
# If direct ffmpeg execution from this container is needed, uncomment and add:
# RUN apt-get update && apt-get install -y ffmpeg libpq-dev gcc && rm -rf /var/lib/apt/lists/*
# Note: libpq-dev and gcc are for psycopg2 if not using binary or if it needs to compile.
# psycopg2-binary should avoid needing gcc and libpq-dev in many cases.

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/alembic.ini
# If env.py for alembic is in root of backend, copy that too.
# COPY env.py /app/env.py # Only if env.py is top-level for alembic and not in ./alembic

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables (can be overridden by docker-compose)
ENV DATABASE_URL="postgresql://postgres:yourpassword@db:5432/resource_manager_db"
# The hostname 'db' will be resolved by Docker Compose if the PostgreSQL service is named 'db'.
ENV PYTHONPATH=/app

# Command to run the application using Uvicorn
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
# It's often better to run Alembic migrations before starting the app.
# This can be done with a startup script.

# Create a startup script
COPY ./scripts/start.sh /start.sh
RUN chmod +x /start.sh

CMD ["/start.sh"]

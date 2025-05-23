# Multimedia Resource Manager

## Project Overview

The Multimedia Resource Manager is a full-stack web application designed to help users import, manage, and analyze collections of multimedia files (images, videos, audio, text). It provides a web interface to browse imported resources, view their details, and see overall statistics about the collection.

The application is containerized using Docker and orchestrated with Docker Compose for ease of development and deployment. It features a Python/FastAPI backend with PostgreSQL for data storage, and a Vue3/TypeScript frontend served by Nginx. A Jenkins CI/CD pipeline is defined for automated deployment.

## Features

*   **Resource Import**: Import multimedia resources by specifying a directory path on the server.
*   **Metadata Extraction**: Automatically extracts metadata from various file types:
    *   Images: name, size, basic EXIF (location placeholder).
    *   Videos: name, duration, codec, bitrate, size.
    *   Audio: name, sample rate, codec, duration, size.
    *   Text & Other: name, size.
*   **Resource Management**: View a list of imported resources and their detailed information, including individual file details.
*   **Statistics**: Display overall statistics such as total number of files, counts by file type, and total video/audio duration.
*   **Database Persistence**: Uses PostgreSQL to store resource metadata.
*   **Containerized**: Fully containerized with Docker for backend, frontend, and database.
*   **CI/CD Ready**: Includes a `Jenkinsfile` for automated deployment.

## Technology Stack

*   **Backend**:
    *   Python 3.9+
    *   FastAPI (web framework)
    *   SQLAlchemy (ORM)
    *   Alembic (database migrations)
    *   PostgreSQL (database)
    *   Uvicorn (ASGI server)
    *   Pillow, ffmpeg-python, exifread (for metadata extraction)
    *   *Assumption*: FFmpeg (command-line tool) must be available in the environment where the backend container runs. The `backend/Dockerfile` has a commented section for its installation.
*   **Frontend**:
    *   Vue 3
    *   TypeScript
    *   Vite (build tool)
    *   Nginx (web server for static files)
*   **Containerization**:
    *   Docker
    *   Docker Compose
*   **CI/CD**:
    *   Jenkins (Declarative Pipeline)

## Prerequisites for Local Development

*   **Docker Desktop** (or Docker Engine + Docker Compose CLI) installed and running.
*   **Git** for cloning the repository.
*   **(Optional)** FFmpeg installed locally if you intend to run and test the backend service outside of Docker and require multimedia file processing.

## Setup and Running Locally (using Docker Compose)

1.  **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory_name>
    ```

2.  **Environment Variable Setup**:
    *   The `docker-compose.yml` file pre-configures most necessary environment variables for local execution.
    *   **Backend**: The `DATABASE_URL` for the backend service is set to `postgresql://admin:supersecret@db:5432/resource_manager_db`, connecting to the `db` service.
    *   **Database (`db` service)**:
        *   `POSTGRES_USER`: `admin`
        *   `POSTGRES_PASSWORD`: `supersecret`
        *   `POSTGRES_DB`: `resource_manager_db`
        These can be customized in `docker-compose.yml`. If changed, update `DATABASE_URL` for the backend and `sqlalchemy.url` in `backend/alembic.ini` (though `DATABASE_URL` env var in `docker-compose.yml` takes precedence for the backend app).

3.  **Build and Run the Application**:
    Use Docker Compose to build images and start services.
    ```bash
    docker-compose up --build -d
    ```
    The `-d` flag runs containers in detached mode. Omit to see logs in the terminal.

4.  **Accessing the Application**:
    *   **Frontend**: `http://localhost:8080`
    *   **Backend API Docs**: `http://localhost:8000/docs` (Swagger UI)

5.  **Stopping the Application**:
    ```bash
    docker-compose down
    ```
    To remove the PostgreSQL data volume (deletes all database data):
    ```bash
    docker-compose down -v
    ```

## Database Migrations

Database migrations are managed by Alembic.
*   **Automatic Application**: The `backend/scripts/start.sh` script (run on backend container start) automatically applies pending migrations using `alembic upgrade head`.
*   **Creating New Migrations**: If SQLAlchemy models (`backend/app/db_models.py`) change during development, generate a new migration:
    ```bash
    docker-compose exec backend alembic revision -m "your_migration_message" --autogenerate
    ```
    Review the generated script in `backend/alembic/versions/`. It will be applied automatically on the next backend start, or apply manually:
    ```bash
    docker-compose exec backend alembic upgrade head
    ```

## CI/CD (Jenkins)

A `Jenkinsfile` is included for CI/CD.
*   **Pipeline**: Checks out code, validates Docker builds, archives the project, copies it to a target server (`scp`), extracts, and then uses `docker-compose` on the server to build and run the application.
*   **Jenkins Configuration**: Requires Docker, SSH capabilities (`sshagent` plugin), and the following Jenkins environment variables/parameters:
    *   `TARGET_SERVER_IP`
    *   `TARGET_SERVER_USER`
    *   `TARGET_SERVER_PATH`
    *   `SSH_CREDENTIALS_ID` (ID of SSH credentials in Jenkins)

## Project Structure

```
.
├── backend/                # FastAPI Backend
│   ├── alembic/            # Alembic migration scripts
│   ├── app/                # Core application (main, crud, models, etc.)
│   ├── scripts/            # Startup scripts (start.sh)
│   ├── tests/              # Backend tests
│   ├── alembic.ini         # Alembic config
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/               # Vue3 Frontend
│   ├── public/
│   ├── src/                # Source code (components, services, etc.)
│   ├── Dockerfile          # Dockerfile (multi-stage with Nginx)
│   ├── nginx.conf          # Nginx config
│   ├── package.json
│   └── vite.config.ts
├── .gitignore
├── docker-compose.yml      # Docker Compose for all services
├── Jenkinsfile             # Jenkins CI/CD pipeline
└── README.md               # This file
```

## Limitations / Future Work

*   **Statistics**: "Changes_last_7_days" and total audio duration in statistics are placeholders.
*   **FFmpeg**: The backend requires FFmpeg for full media metadata. The `backend/Dockerfile` has a commented line for its installation. Ensure FFmpeg is in the backend container's environment.
*   **Error Handling**: Frontend API error handling can be improved.
*   **Security**: Default passwords in `docker-compose.yml` are for local use only. HTTPS is not configured (typically via a reverse proxy in production).
*   **Testing**: Basic backend unit tests exist. More comprehensive tests (unit, integration) are needed. No frontend tests are included.
*   **Scalability**: Current setup is for single-node. Consider Kubernetes for larger deployments.
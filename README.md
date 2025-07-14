# Portal Flask Application - Docker Setup

This is a Flask web application for personnel data management and automation.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

### Using Docker Compose (Recommended)

1. Build and run the application:
```bash
docker-compose up --build
```

2. Access the application at: http://localhost:5000

3. To run in background:
```bash
docker-compose up -d --build
```

4. To stop the application:
```bash
docker-compose down
```

### Using Docker directly

1. Build the Docker image:
```bash
docker build -t portal-app .
```

2. Run the container:
```bash
docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads portal-app
```

## Features

- File upload functionality for CSV files
- Dashboard for data visualization
- IKH and IKK automation processing
- Personnel data management

## Directory Structure

```
/home/dan/Portal/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── .dockerignore         # Docker ignore file
├── personnel_list.csv    # Sample data file
├── static/               # Static files and automation scripts
├── templates/            # HTML templates
└── uploads/              # File upload directory
```

## Environment Variables

- `FLASK_ENV`: Set to 'production' in Docker
- `DISPLAY`: Set to ':99' for virtual display (required for automation scripts)

## Volumes

- `./uploads:/app/uploads` - Persistent storage for uploaded files
- `./automation.log:/app/automation.log` - Automation log file

## Ports

- Port 5000 is exposed for the Flask application

## Notes

- The application includes Xvfb for running GUI automation scripts in a headless environment
- Upload directory is mounted as a volume to persist uploaded files
- The application runs in production mode when containerized

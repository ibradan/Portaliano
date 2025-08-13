# Portaliano Docker Deployment Guide

## 🐳 Overview

This guide covers the complete Docker setup for Portaliano automation system, including development, testing, and production deployments.

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 2GB RAM available
- 5GB free disk space

## 🚀 Quick Start

### 1. Build the Image

```bash
# Build with default settings
./docker-build.sh

# Build with specific tag
./docker-build.sh -t v1.0.0

# Build with cleanup and no testing
./docker-build.sh -c --no-test
```

### 2. Run Development Environment

```bash
# Start development environment (with browser visible)
docker-compose up -d

# View logs
docker-compose logs -f portaliano

# Stop
docker-compose down
```

### 3. Run Production Environment

```bash
# Set production secret key
export SECRET_KEY="your-secure-secret-key-here"

# Start production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Check status
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `FLASK_DEBUG` | `0` | Enable Flask debug mode |
| `HEADLESS_MODE` | `true` | Browser headless mode |
| `SLOW_MO` | `0` | Browser action delay (ms) |
| `SECRET_KEY` | Auto-generated | Flask secret key |
| `MAX_WORKERS` | `4` | Thread pool workers |
| `MAX_FILE_SIZE` | `5242880` | Max upload size (5MB) |

### Browser Configuration

The application uses `browser_config.py` for browser settings:

- **Development**: Browser visible, slower actions
- **Production**: Headless mode, fastest execution

Override via environment variables:
```bash
HEADLESS_MODE=false SLOW_MO=100 docker-compose up
```

## 📁 File Structure

```
Portaliano/
├── Dockerfile                 # Multi-stage build
├── docker-compose.yml         # Base configuration
├── docker-compose.override.yml # Development overrides
├── docker-compose.prod.yml    # Production overrides
├── .dockerignore             # Build exclusions
├── docker-build.sh           # Build script
├── app.py                    # Main application
├── browser_config.py         # Browser settings
├── requirements.txt          # Python dependencies
├── static/                   # Static files
├── templates/                # HTML templates
├── uploads/                  # Upload directory
└── logs/                     # Log files
```

## 🏗️ Build Process

### Multi-Stage Build

1. **Builder Stage**: Install dependencies and Playwright
2. **Production Stage**: Minimal runtime image

### Size Optimization

- Excludes virtual environment (~136MB)
- Installs only Chromium browser
- Removes build tools in production
- Uses `.dockerignore` for exclusions

### Security Features

- Non-root user (`appuser`)
- Read-only filesystem (production)
- No new privileges
- Resource limits
- Health checks

## 🔍 Monitoring & Debugging

### Health Checks

```bash
# Check container health
docker-compose ps

# View health check logs
docker inspect portaliano-app | grep -A 10 Health
```

### Logs

```bash
# Application logs
docker-compose logs -f portaliano

# Container logs
docker logs portaliano-app

# Follow logs with timestamps
docker-compose logs -f --timestamps portaliano
```

### Resource Usage

```bash
# Container stats
docker stats portaliano-app

# Resource limits
docker inspect portaliano-app | grep -A 5 "Memory\|Cpu"
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Container Won't Start

```bash
# Check logs
docker-compose logs portaliano

# Check if port is in use
netstat -tulpn | grep :5000

# Remove and recreate
docker-compose down
docker-compose up --force-recreate
```

#### 2. Browser Issues

```bash
# Check Playwright installation
docker exec portaliano-app playwright --version

# Reinstall browsers
docker exec portaliano-app playwright install chromium
```

#### 3. Permission Issues

```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/
```

#### 4. Memory Issues

```bash
# Check memory usage
docker stats portaliano-app

# Increase memory limit in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 4G
```

### Debug Mode

```bash
# Run with debug settings
HEADLESS_MODE=false SLOW_MO=500 docker-compose up

# Access container shell
docker exec -it portaliano-app /bin/bash
```

## 📊 Performance Optimization

### Resource Limits

```yaml
deploy:
  resources:
    limits:
      memory: 2G
      cpus: '1.0'
    reservations:
      memory: 512M
      cpus: '0.5'
```

### Browser Optimization

- Headless mode for production
- Minimal browser arguments
- No unnecessary browser features

### Image Size

- Multi-stage build reduces size by ~60%
- Excludes development files
- Minimal runtime dependencies

## 🔄 CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: |
          docker build -t portaliano:${{ github.sha }} .
      - name: Push to registry
        run: |
          docker tag portaliano:${{ github.sha }} your-registry/portaliano:latest
          docker push your-registry/portaliano:latest
```

## 🚀 Production Deployment

### 1. Environment Setup

```bash
# Create production environment file
cat > .env.production << EOF
SECRET_KEY=your-very-secure-secret-key-here
FLASK_ENV=production
HEADLESS_MODE=true
SLOW_MO=0
EOF
```

### 2. Deploy

```bash
# Load environment
set -a; source .env.production; set +a

# Deploy production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Verify deployment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml ps
```

### 3. Monitoring

```bash
# Set up monitoring
docker-compose -f docker-compose.yml -f docker-compose.prod.yml logs -f

# Check health
curl -f http://localhost:5000/dashboard
```

## 📝 Maintenance

### Regular Tasks

1. **Update Dependencies**
   ```bash
   # Update requirements.txt
   docker run --rm -v $(pwd):/app python:3.10-slim pip freeze > requirements.txt
   ```

2. **Clean Up Images**
   ```bash
   # Remove old images
   docker image prune -f
   docker system prune -f
   ```

3. **Backup Data**
   ```bash
   # Backup uploads
   tar -czf uploads-backup-$(date +%Y%m%d).tar.gz uploads/
   ```

### Updates

```bash
# Pull latest changes
git pull

# Rebuild and deploy
./docker-build.sh -c
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## 🔐 Security Considerations

1. **Secret Management**: Use environment variables for secrets
2. **Network Security**: Limit exposed ports
3. **Resource Limits**: Prevent resource exhaustion
4. **Non-root User**: Container runs as non-root
5. **Read-only Filesystem**: Production containers are read-only
6. **Regular Updates**: Keep base images updated

## 📞 Support

For issues and questions:

1. Check the troubleshooting section
2. Review container logs
3. Verify environment configuration
4. Test with development settings

---

**Last Updated**: $(date)
**Version**: 1.0.0

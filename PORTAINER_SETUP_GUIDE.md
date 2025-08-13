# Portainer Setup Guide for Portaliano

## 🐳 Overview

This guide will help you set up Portainer to manage your Portaliano Docker containers with a beautiful web interface.

## 🚀 Quick Setup

### Automated Setup (Recommended)

```bash
# Full setup (Portainer + Portaliano)
./setup-portainer.sh

# Install only Portainer
./setup-portainer.sh --portainer-only

# Deploy only Portaliano (skip build)
./setup-portainer.sh --portaliano-only --skip-build
```

### Manual Setup

If you prefer manual setup, follow these steps:

## 📋 Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- At least 2GB RAM available
- 5GB free disk space

## 🔧 Step-by-Step Setup

### 1. Install Portainer

```bash
# Create Portainer volume
docker volume create portainer_data

# Run Portainer
docker run -d \
  -p 9000:9000 \
  --name=portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 2. Deploy Portaliano

```bash
# Build Portaliano image
docker build -t portaliano:latest .

# Deploy with docker-compose
docker-compose up -d
```

### 3. Verify Installation

```bash
# Check running containers
docker ps

# Test Portaliano
curl -f http://localhost:5000/dashboard

# Test Portainer
curl -f http://localhost:9000
```

## 🌐 Access Your Applications

### Portainer Web Interface
- **URL**: http://localhost:9000
- **First Time**: Create admin account
- **Environment**: Select "Local Docker Environment"

### Portaliano Application
- **URL**: http://localhost:5000
- **Dashboard**: http://localhost:5000/dashboard
- **IKH Automation**: http://localhost:5000/ikh
- **IKK Automation**: http://localhost:5000/ikk

## 📊 Portainer Features for Portaliano

### Container Management
- ✅ **View Container Status**: Real-time status monitoring
- ✅ **Start/Stop/Restart**: Easy container control
- ✅ **View Logs**: Access application logs
- ✅ **Resource Monitoring**: CPU, memory, network usage
- ✅ **Container Shell**: Access container terminal

### Volume Management
- ✅ **Uploads Volume**: Persistent file storage
- ✅ **Logs Volume**: Application log persistence
- ✅ **Portainer Data**: Configuration persistence

### Network Management
- ✅ **Bridge Network**: Container communication
- ✅ **Port Mapping**: External access configuration
- ✅ **Health Checks**: Automatic health monitoring

## 🎯 Using Portainer with Portaliano

### 1. First Login to Portainer

1. Open http://localhost:9000
2. Create admin account (first time only)
3. Select "Local Docker Environment"
4. Click "Connect"

### 2. Navigate to Containers

1. Click "Containers" in the left sidebar
2. You'll see:
   - `portaliano-app` (Portaliano application)
   - `portainer` (Portainer itself)

### 3. Manage Portaliano Container

#### View Container Details
- Click on `portaliano-app`
- View container information, logs, and stats

#### Access Container Logs
- Click "Logs" tab
- View real-time application logs
- Filter logs by time or content

#### Monitor Resources
- Click "Stats" tab
- Monitor CPU, memory, and network usage
- View historical performance data

#### Execute Commands
- Click "Console" tab
- Access container shell
- Run commands inside the container

#### Restart Container
- Click "Actions" → "Restart"
- Useful for applying configuration changes

### 4. Manage Volumes

1. Click "Volumes" in the left sidebar
2. You'll see:
   - `portaliano_portaliano-uploads` (Upload files)
   - `portaliano_portaliano-logs` (Application logs)
   - `portainer_data` (Portainer configuration)

### 5. Monitor Networks

1. Click "Networks" in the left sidebar
2. View `portaliano_portaliano-network`
3. See container connectivity

## 🔧 Configuration Options

### Environment Variables

You can modify Portaliano behavior through environment variables:

```yaml
# In docker-compose.yml
environment:
  - FLASK_ENV=production
  - HEADLESS_MODE=true
  - SLOW_MO=0
  - MAX_WORKERS=4
```

### Resource Limits

Set resource limits in Portainer:

1. Go to Container → `portaliano-app`
2. Click "Actions" → "Duplicate/Edit"
3. Set resource limits:
   - Memory: 2GB
   - CPU: 1.0 cores

### Health Checks

Portaliano includes health checks:

```bash
# Check health status
docker inspect portaliano-app | grep -A 10 Health

# Manual health check
curl -f http://localhost:5000/dashboard
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. Portainer Won't Start

```bash
# Check if port 9000 is in use
netstat -tulpn | grep :9000

# Remove and recreate Portainer
docker stop portainer
docker rm portainer
docker volume rm portainer_data
./setup-portainer.sh --portainer-only
```

#### 2. Portaliano Won't Start

```bash
# Check logs
docker logs portaliano-app

# Rebuild image
docker build -t portaliano:latest .

# Restart container
docker-compose down
docker-compose up -d
```

#### 3. Browser Issues

```bash
# Check Playwright installation
docker exec portaliano-app playwright --version

# Reinstall browsers
docker exec portaliano-app playwright install chromium
```

#### 4. Permission Issues

```bash
# Fix upload directory permissions
sudo chown -R 1000:1000 uploads/
sudo chmod -R 755 uploads/
```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
# Run with debug settings
HEADLESS_MODE=false SLOW_MO=500 docker-compose up

# Access container shell
docker exec -it portaliano-app /bin/bash
```

## 📈 Monitoring & Maintenance

### Regular Tasks

1. **Check Container Health**
   - Portainer → Containers → Health status
   - Look for any unhealthy containers

2. **Monitor Resource Usage**
   - Portainer → Containers → Stats
   - Watch for high CPU/memory usage

3. **Review Logs**
   - Portainer → Containers → Logs
   - Check for errors or warnings

4. **Backup Data**
   - Portainer → Volumes → Backup
   - Export important data

### Updates

```bash
# Update Portaliano
git pull
./setup-portainer.sh --portaliano-only

# Update Portainer
docker pull portainer/portainer-ce:latest
docker stop portainer
docker rm portainer
./setup-portainer.sh --portainer-only
```

## 🔐 Security Considerations

### Portainer Security
- Change default admin password
- Use HTTPS in production
- Restrict access to Portainer interface
- Regular security updates

### Portaliano Security
- Non-root container user
- Read-only filesystem (production)
- Resource limits
- Network isolation

## 🎉 Benefits of Using Portainer

### 1. **Easy Management**
- Web-based interface
- No command line needed
- Intuitive navigation

### 2. **Real-time Monitoring**
- Live container stats
- Resource usage tracking
- Health status monitoring

### 3. **Quick Actions**
- One-click restart
- Easy log access
- Simple configuration changes

### 4. **Visual Interface**
- Container status overview
- Network topology
- Volume management

### 5. **Troubleshooting**
- Integrated logs viewer
- Container console access
- Error detection

## 📞 Support

For issues and questions:

1. Check this guide's troubleshooting section
2. Review Portainer documentation
3. Check container logs in Portainer
4. Test with debug mode

---

**Setup Completed**: $(date)
**Version**: 1.0.0
**Status**: ✅ Ready for Production

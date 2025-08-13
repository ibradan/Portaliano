#!/bin/bash

# Portaliano Portainer Setup Script
# =================================
# Setup Portainer and configure Portaliano for easy management

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        print_error "This script should not be run as root"
        exit 1
    fi
}

# Check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Install Portainer
install_portainer() {
    print_status "Installing Portainer..."
    
    # Create Portainer volume if not exists
    if ! docker volume ls | grep -q portainer_data; then
        docker volume create portainer_data
        print_success "Portainer volume created"
    fi
    
    # Stop and remove existing Portainer if running
    if docker ps -q -f name=portainer | grep -q .; then
        print_status "Stopping existing Portainer..."
        docker stop portainer
        docker rm portainer
    fi
    
    # Run Portainer
    docker run -d \
        -p 9000:9000 \
        --name=portainer \
        --restart=always \
        -v /var/run/docker.sock:/var/run/docker.sock \
        -v portainer_data:/data \
        portainer/portainer-ce:latest
    
    print_success "Portainer installed and started"
}

# Build and deploy Portaliano
deploy_portaliano() {
    print_status "Building Portaliano application..."
    
    # Build the image
    docker build -t portaliano:latest .
    
    if [[ $? -eq 0 ]]; then
        print_success "Portaliano image built successfully"
    else
        print_error "Failed to build Portaliano image"
        exit 1
    fi
    
    print_status "Deploying Portaliano..."
    
    # Stop existing container if running
    if docker ps -q -f name=portaliano-app | grep -q .; then
        print_status "Stopping existing Portaliano container..."
        docker-compose down
    fi
    
    # Start Portaliano
    docker-compose up -d
    
    print_success "Portaliano deployed successfully"
}

# Wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for Portainer
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:9000 &> /dev/null; then
            print_success "Portainer is ready"
            break
        fi
        
        print_status "Waiting for Portainer... (attempt $attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        print_warning "Portainer may not be fully ready yet"
    fi
    
    # Wait for Portaliano
    attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:5000/dashboard &> /dev/null; then
            print_success "Portaliano is ready"
            break
        fi
        
        print_status "Waiting for Portaliano... (attempt $attempt/$max_attempts)"
        sleep 5
        ((attempt++))
    done
    
    if [[ $attempt -gt $max_attempts ]]; then
        print_warning "Portaliano may not be fully ready yet"
    fi
}

# Show final information
show_info() {
    echo ""
    echo "🎉 Setup completed successfully!"
    echo "=================================="
    echo ""
    
    print_status "Services Status:"
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    print_success "Access Information:"
    echo "  🌐 Portainer: http://localhost:9000"
    echo "  📊 Portaliano: http://localhost:5000"
    echo "  📋 Portaliano Dashboard: http://localhost:5000/dashboard"
    echo ""
    
    print_status "Portainer Setup Instructions:"
    echo "  1. Open http://localhost:9000 in your browser"
    echo "  2. Create admin account (first time only)"
    echo "  3. Select 'Local Docker Environment'"
    echo "  4. You'll see both Portainer and Portaliano containers"
    echo ""
    
    print_status "Portaliano Features in Portainer:"
    echo "  ✅ View container logs"
    echo "  ✅ Monitor resource usage"
    echo "  ✅ Restart/stop containers"
    echo "  ✅ Access container shell"
    echo "  ✅ View container details"
    echo ""
    
    print_warning "Important Notes:"
    echo "  • Portaliano runs on port 5000"
    echo "  • Portainer runs on port 9000"
    echo "  • Both services restart automatically"
    echo "  • Data is persisted in Docker volumes"
    echo ""
}

# Show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  --portainer-only    Install only Portainer"
    echo "  --portaliano-only   Deploy only Portaliano"
    echo "  --skip-build        Skip building Portaliano image"
    echo ""
    echo "Examples:"
    echo "  $0                  # Full setup (Portainer + Portaliano)"
    echo "  $0 --portainer-only # Install only Portainer"
    echo "  $0 --skip-build     # Setup without rebuilding image"
}

# Parse command line arguments
PORTAINER_ONLY=false
PORTALIANO_ONLY=false
SKIP_BUILD=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        --portainer-only)
            PORTAINER_ONLY=true
            shift
            ;;
        --portaliano-only)
            PORTALIANO_ONLY=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo "🐳 Portaliano Portainer Setup"
    echo "=============================="
    echo ""
    
    check_root
    check_prerequisites
    
    if [[ "$PORTAINER_ONLY" == "true" ]]; then
        print_status "Installing Portainer only..."
        install_portainer
    elif [[ "$PORTALIANO_ONLY" == "true" ]]; then
        print_status "Deploying Portaliano only..."
        if [[ "$SKIP_BUILD" != "true" ]]; then
            deploy_portaliano
        else
            docker-compose up -d
        fi
    else
        print_status "Full setup (Portainer + Portaliano)..."
        install_portainer
        if [[ "$SKIP_BUILD" != "true" ]]; then
            deploy_portaliano
        else
            docker-compose up -d
        fi
    fi
    
    wait_for_services
    show_info
}

# Run main function
main "$@"

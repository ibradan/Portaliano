#!/bin/bash

# Portaliano Production Deployment Script
# ======================================
# Automated deployment for production environment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
COMPOSE_FILES="-f docker-compose.yml -f docker-compose.prod.yml"
SERVICE_NAME="portaliano"
CONTAINER_NAME="portaliano-app"

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

# Check environment
check_environment() {
    print_status "Checking environment..."
    
    if [[ -z "$SECRET_KEY" ]]; then
        print_warning "SECRET_KEY not set, using default"
        export SECRET_KEY="dev-key-change-in-production-$(date +%s)"
    fi
    
    if [[ -z "$FLASK_ENV" ]]; then
        export FLASK_ENV="production"
    fi
    
    print_success "Environment configured"
}

# Backup current deployment
backup_current() {
    print_status "Creating backup..."
    
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        BACKUP_DIR="backup-$(date +%Y%m%d-%H%M%S)"
        mkdir -p $BACKUP_DIR
        
        # Backup uploads
        if [[ -d "uploads" ]]; then
            tar -czf "$BACKUP_DIR/uploads.tar.gz" uploads/
        fi
        
        # Backup logs
        if [[ -d "logs" ]]; then
            tar -czf "$BACKUP_DIR/logs.tar.gz" logs/
        fi
        
        print_success "Backup created in $BACKUP_DIR"
    else
        print_status "No running container to backup"
    fi
}

# Stop current deployment
stop_current() {
    print_status "Stopping current deployment..."
    
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        docker-compose $COMPOSE_FILES down
        print_success "Current deployment stopped"
    else
        print_status "No running deployment found"
    fi
}

# Build new image
build_image() {
    print_status "Building new Docker image..."
    
    if [[ "$1" == "--no-build" ]]; then
        print_status "Skipping build (--no-build flag)"
        return 0
    fi
    
    ./docker-build.sh -c --no-test
    
    if [[ $? -eq 0 ]]; then
        print_success "Docker image built successfully"
    else
        print_error "Docker build failed"
        exit 1
    fi
}

# Deploy new version
deploy_new() {
    print_status "Deploying new version..."
    
    # Create required directories
    mkdir -p uploads logs
    
    # Set proper permissions
    sudo chown -R 1000:1000 uploads/ logs/ 2>/dev/null || true
    
    # Start deployment
    docker-compose $COMPOSE_FILES up -d
    
    if [[ $? -eq 0 ]]; then
        print_success "Deployment started"
    else
        print_error "Deployment failed"
        exit 1
    fi
}

# Wait for deployment to be ready
wait_for_ready() {
    print_status "Waiting for deployment to be ready..."
    
    local max_attempts=30
    local attempt=1
    
    while [[ $attempt -le $max_attempts ]]; do
        if curl -f http://localhost:5000/dashboard &> /dev/null; then
            print_success "Deployment is ready"
            return 0
        fi
        
        print_status "Attempt $attempt/$max_attempts - waiting..."
        sleep 10
        ((attempt++))
    done
    
    print_error "Deployment failed to become ready"
    return 1
}

# Check deployment health
check_health() {
    print_status "Checking deployment health..."
    
    # Check container status
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        print_success "Container is running"
    else
        print_error "Container is not running"
        return 1
    fi
    
    # Check health status
    local health_status=$(docker inspect --format='{{.State.Health.Status}}' $CONTAINER_NAME 2>/dev/null || echo "no-health-check")
    
    if [[ "$health_status" == "healthy" ]]; then
        print_success "Health check passed"
    elif [[ "$health_status" == "no-health-check" ]]; then
        print_warning "No health check configured"
    else
        print_warning "Health check status: $health_status"
    fi
    
    # Check application endpoint
    if curl -f http://localhost:5000/dashboard &> /dev/null; then
        print_success "Application is responding"
    else
        print_error "Application is not responding"
        return 1
    fi
}

# Show deployment info
show_info() {
    print_status "Deployment information:"
    echo ""
    
    # Container info
    docker ps -f name=$CONTAINER_NAME --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    
    # Resource usage
    print_status "Resource usage:"
    docker stats $CONTAINER_NAME --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"
    echo ""
    
    # Environment info
    print_status "Environment:"
    echo "  FLASK_ENV: $FLASK_ENV"
    echo "  HEADLESS_MODE: ${HEADLESS_MODE:-true}"
    echo "  SLOW_MO: ${SLOW_MO:-0}"
    echo "  MAX_WORKERS: ${MAX_WORKERS:-4}"
    echo ""
    
    # Access info
    print_success "Application is available at:"
    echo "  🌐 http://localhost:5000"
    echo "  📊 Dashboard: http://localhost:5000/dashboard"
    echo ""
}

# Rollback function
rollback() {
    print_warning "Rolling back deployment..."
    
    # Stop current deployment
    docker-compose $COMPOSE_FILES down
    
    # Start previous deployment (if exists)
    if docker images portaliano:previous &> /dev/null; then
        docker tag portaliano:previous portaliano:latest
        docker-compose $COMPOSE_FILES up -d
        print_success "Rollback completed"
    else
        print_error "No previous image found for rollback"
        exit 1
    fi
}

# Show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  deploy              Deploy new version (default)"
    echo "  rollback            Rollback to previous version"
    echo "  status              Show deployment status"
    echo "  logs                Show application logs"
    echo ""
    echo "Options:"
    echo "  --no-build          Skip building new image"
    echo "  --no-backup         Skip backup creation"
    echo "  -h, --help          Show this help message"
    echo ""
    echo "Environment Variables:"
    echo "  SECRET_KEY          Flask secret key"
    echo "  FLASK_ENV           Flask environment (default: production)"
    echo "  HEADLESS_MODE       Browser headless mode (default: true)"
    echo "  SLOW_MO             Browser delay in ms (default: 0)"
    echo ""
    echo "Examples:"
    echo "  $0                  # Deploy with build"
    echo "  $0 --no-build       # Deploy without building"
    echo "  $0 status           # Show status"
    echo "  $0 rollback         # Rollback deployment"
}

# Parse command line arguments
COMMAND="deploy"
NO_BUILD=false
NO_BACKUP=false

while [[ $# -gt 0 ]]; do
    case $1 in
        deploy|rollback|status|logs)
            COMMAND="$1"
            shift
            ;;
        --no-build)
            NO_BUILD=true
            shift
            ;;
        --no-backup)
            NO_BACKUP=true
            shift
            ;;
        -h|--help)
            show_usage
            exit 0
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
    echo "🚀 Portaliano Production Deployment"
    echo "==================================="
    echo ""
    
    check_root
    check_prerequisites
    check_environment
    
    case $COMMAND in
        deploy)
            if [[ "$NO_BACKUP" != "true" ]]; then
                backup_current
            fi
            
            # Tag current image as previous
            if docker images portaliano:latest &> /dev/null; then
                docker tag portaliano:latest portaliano:previous
            fi
            
            stop_current
            build_image $([[ "$NO_BUILD" == "true" ]] && echo "--no-build")
            deploy_new
            wait_for_ready
            check_health
            show_info
            ;;
        rollback)
            rollback
            wait_for_ready
            check_health
            show_info
            ;;
        status)
            check_health
            show_info
            ;;
        logs)
            docker-compose $COMPOSE_FILES logs -f $SERVICE_NAME
            ;;
        *)
            print_error "Unknown command: $COMMAND"
            show_usage
            exit 1
            ;;
    esac
    
    print_success "Deployment process completed!"
}

# Run main function
main "$@"

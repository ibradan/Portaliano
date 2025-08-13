#!/bin/bash

# Portaliano Docker Build Script
# ==============================
# Optimized multi-stage build with size reduction and security improvements

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="portaliano"
TAG="latest"
BUILD_CONTEXT="."
DOCKERFILE="Dockerfile"

# Function to print colored output
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

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        print_error "Docker daemon is not running"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to clean up old images
cleanup_old_images() {
    print_status "Cleaning up old images..."
    
    # Remove dangling images
    docker image prune -f
    
    # Remove old portaliano images (keep only latest)
    docker images ${IMAGE_NAME} --format "table {{.Repository}}:{{.Tag}}\t{{.Size}}" | grep -v "latest" | awk '{print $1}' | xargs -r docker rmi -f
    
    print_success "Cleanup completed"
}

# Function to build the image
build_image() {
    print_status "Building Docker image..."
    print_status "Image: ${IMAGE_NAME}:${TAG}"
    print_status "Context: ${BUILD_CONTEXT}"
    print_status "Dockerfile: ${DOCKERFILE}"
    
    # Build with progress and cache optimization
    docker build \
        --progress=plain \
        --no-cache \
        --build-arg BUILDKIT_INLINE_CACHE=1 \
        -f "${DOCKERFILE}" \
        -t "${IMAGE_NAME}:${TAG}" \
        "${BUILD_CONTEXT}"
    
    if [ $? -eq 0 ]; then
        print_success "Docker image built successfully"
    else
        print_error "Docker build failed"
        exit 1
    fi
}

# Function to show image information
show_image_info() {
    print_status "Image information:"
    docker images ${IMAGE_NAME}:${TAG} --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}\t{{.CreatedAt}}"
    
    # Show image layers and size breakdown
    print_status "Image size breakdown:"
    docker history ${IMAGE_NAME}:${TAG} --format "table {{.CreatedBy}}\t{{.Size}}"
}

# Function to test the container
test_container() {
    print_status "Testing container..."
    
    # Run container in background
    CONTAINER_ID=$(docker run -d -p 5000:5000 --name portaliano-test ${IMAGE_NAME}:${TAG})
    
    if [ $? -eq 0 ]; then
        print_success "Container started successfully"
        
        # Wait for container to be ready
        print_status "Waiting for container to be ready..."
        sleep 10
        
        # Test health check
        if curl -f http://localhost:5000/dashboard &> /dev/null; then
            print_success "Health check passed"
        else
            print_warning "Health check failed - container may still be starting"
        fi
        
        # Stop and remove test container
        docker stop ${CONTAINER_ID} &> /dev/null
        docker rm ${CONTAINER_ID} &> /dev/null
        print_success "Test container cleaned up"
    else
        print_error "Container test failed"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -h, --help          Show this help message"
    echo "  -t, --tag TAG       Set image tag (default: latest)"
    echo "  -c, --clean         Clean up old images before building"
    echo "  --no-test           Skip container testing"
    echo "  --no-cleanup        Skip cleanup of old images"
    echo ""
    echo "Examples:"
    echo "  $0                  # Build with default settings"
    echo "  $0 -t v1.0.0        # Build with specific tag"
    echo "  $0 -c --no-test     # Clean and build without testing"
}

# Parse command line arguments
CLEANUP=false
TEST_CONTAINER=true

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_usage
            exit 0
            ;;
        -t|--tag)
            TAG="$2"
            shift 2
            ;;
        -c|--clean)
            CLEANUP=true
            shift
            ;;
        --no-test)
            TEST_CONTAINER=false
            shift
            ;;
        --no-cleanup)
            CLEANUP=false
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
    echo "🐳 Portaliano Docker Build Script"
    echo "=================================="
    echo ""
    
    check_prerequisites
    
    if [ "$CLEANUP" = true ]; then
        cleanup_old_images
    fi
    
    build_image
    show_image_info
    
    if [ "$TEST_CONTAINER" = true ]; then
        test_container
    fi
    
    echo ""
    print_success "Build process completed successfully!"
    echo ""
    echo "Next steps:"
    echo "  • Run: docker-compose up -d"
    echo "  • Or: docker run -p 5000:5000 ${IMAGE_NAME}:${TAG}"
    echo "  • Access: http://localhost:5000"
}

# Run main function
main "$@"

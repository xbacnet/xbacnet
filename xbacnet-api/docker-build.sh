#!/bin/bash

# XBACnet API Docker Build Script
# This script builds and runs the XBACnet API Docker container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
IMAGE_NAME="xbacnet-api"
CONTAINER_NAME="xbacnet-api"
PORT="8000"
PYTHON_VERSION="3.10"

# Functions
print_info() {
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

# Check if Docker is installed
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
}

# Build Docker image
build_image() {
    print_info "Building Docker image: $IMAGE_NAME (Python $PYTHON_VERSION)"
    docker build -t $IMAGE_NAME .
    print_success "Docker image built successfully"
}

# Run Docker container
run_container() {
    print_info "Running Docker container: $CONTAINER_NAME"

    # Stop existing container if running
    if docker ps -q -f name=$CONTAINER_NAME | grep -q .; then
        print_warning "Stopping existing container"
        docker stop $CONTAINER_NAME
        docker rm $CONTAINER_NAME
    fi

    # Run new container
    docker run -d \
        --name $CONTAINER_NAME \
        -p $PORT:8000 \
        -e XBACNET_DB_HOST=localhost \
        -e XBACNET_DB_USER=root \
        -e XBACNET_DB_PASSWORD= \
        -e XBACNET_DB_NAME=xbacnet \
        -v $(pwd)/logs:/app/logs \
        -v $(pwd)/tmp:/app/tmp \
        $IMAGE_NAME

    print_success "Container started successfully"
    print_info "API is available at: http://localhost:$PORT"
    print_info "Health check: http://localhost:$PORT/api/health"
}

# Stop Docker container
stop_container() {
    print_info "Stopping Docker container: $CONTAINER_NAME"
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
    print_success "Container stopped successfully"
}

# Show container logs
show_logs() {
    print_info "Showing container logs"
    docker logs -f $CONTAINER_NAME
}

# Show container status
show_status() {
    print_info "Container status:"
    docker ps -f name=$CONTAINER_NAME
}

# Main menu
show_menu() {
    echo
    echo "XBACnet API Docker Management"
    echo "============================="
    echo "1. Build Docker image"
    echo "2. Run container"
    echo "3. Stop container"
    echo "4. Show logs"
    echo "5. Show status"
    echo "6. Build and run"
    echo "7. Exit"
    echo
}

# Main execution
main() {
    check_docker

    if [ $# -eq 0 ]; then
        # Interactive mode
        while true; do
            show_menu
            read -p "Please select an option (1-7): " choice

            case $choice in
                1)
                    build_image
                    ;;
                2)
                    run_container
                    ;;
                3)
                    stop_container
                    ;;
                4)
                    show_logs
                    ;;
                5)
                    show_status
                    ;;
                6)
                    build_image
                    run_container
                    ;;
                7)
                    print_info "Goodbye!"
                    exit 0
                    ;;
                *)
                    print_error "Invalid option. Please try again."
                    ;;
            esac

            echo
            read -p "Press Enter to continue..."
        done
    else
        # Command line mode
        case $1 in
            build)
                build_image
                ;;
            run)
                run_container
                ;;
            stop)
                stop_container
                ;;
            logs)
                show_logs
                ;;
            status)
                show_status
                ;;
            build-run)
                build_image
                run_container
                ;;
            *)
                echo "Usage: $0 [build|run|stop|logs|status|build-run]"
                echo "Or run without arguments for interactive mode"
                exit 1
                ;;
        esac
    fi
}

# Run main function
main "$@"

#!/bin/bash

# XBACnet Web Management Interface Startup Script
# This script helps you get started with the XBACnet Web Interface

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check if Node.js is installed
check_nodejs() {
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed. Please install Node.js 16+ first."
        print_status "Visit: https://nodejs.org/"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 16 ]; then
        print_error "Node.js version 16+ is required. Current version: $(node -v)"
        exit 1
    fi
    
    print_success "Node.js $(node -v) is installed"
}

# Check if npm is installed
check_npm() {
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed. Please install npm first."
        exit 1
    fi
    
    print_success "npm $(npm -v) is installed"
}

# Check if XBACnet API is running
check_api() {
    print_status "Checking XBACnet API server..."
    
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        print_success "XBACnet API server is running on http://localhost:8000"
    else
        print_warning "XBACnet API server is not running on http://localhost:8000"
        print_status "Please start the XBACnet API server first:"
        print_status "  cd ../xbacnet-api && python run.py"
        echo
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    if [ ! -d "node_modules" ]; then
        npm install
        print_success "Dependencies installed successfully"
    else
        print_status "Dependencies already installed"
    fi
}

# Setup environment
setup_environment() {
    if [ ! -f ".env" ]; then
        print_status "Setting up environment configuration..."
        cp env.example .env
        print_success "Environment configuration created (.env)"
        print_status "You can edit .env file to customize settings"
    else
        print_status "Environment configuration already exists"
    fi
}

# Start development server
start_dev_server() {
    print_status "Starting development server..."
    print_success "XBACnet Web Interface will be available at: http://localhost:3000"
    print_status "Default login credentials:"
    print_status "  Username: administrator"
    print_status "  Password: !BACnetPro1"
    echo
    
    npm run dev
}

# Main execution
main() {
    echo "=========================================="
    echo "  XBACnet Web Management Interface"
    echo "=========================================="
    echo
    
    # Check prerequisites
    check_nodejs
    check_npm
    check_api
    
    # Setup project
    install_dependencies
    setup_environment
    
    echo
    print_success "Setup completed successfully!"
    echo
    
    # Start server
    start_dev_server
}

# Handle script arguments
case "${1:-}" in
    --help|-h)
        echo "XBACnet Web Management Interface Startup Script"
        echo
        echo "Usage: $0 [OPTIONS]"
        echo
        echo "Options:"
        echo "  --help, -h     Show this help message"
        echo "  --build        Build for production"
        echo "  --docker       Build and run with Docker"
        echo "  --check        Check prerequisites only"
        echo
        echo "Examples:"
        echo "  $0              Start development server"
        echo "  $0 --build      Build for production"
        echo "  $0 --docker     Run with Docker"
        echo "  $0 --check      Check if everything is ready"
        exit 0
        ;;
    --build)
        print_status "Building for production..."
        npm run build
        print_success "Build completed! Files are in the 'dist' directory."
        exit 0
        ;;
    --docker)
        print_status "Building Docker image..."
        docker build -t xbacnet-web .
        print_success "Docker image built successfully!"
        print_status "To run the container:"
        print_status "  docker run -p 3000:3000 xbacnet-web"
        exit 0
        ;;
    --check)
        check_nodejs
        check_npm
        check_api
        print_success "All prerequisites are satisfied!"
        exit 0
        ;;
    *)
        main
        ;;
esac

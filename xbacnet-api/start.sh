#!/bin/bash

# XBACnet API Startup Script
# This script starts the XBACnet REST API server

echo "Starting XBACnet API Server..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p tmp

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "Please edit .env file with your database settings before starting the server."
    exit 1
fi

# Start the server
echo "Starting XBACnet API server..."
python run.py

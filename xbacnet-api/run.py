#!/usr/bin/env python3
"""
XBACnet API Server Startup Script

This script starts the XBACnet REST API server using Gunicorn.
It handles server initialization, database connection setup, and
provides command-line options for configuration.

Author: XBACnet Team
Date: 2024
"""

import os
import sys
import logging
import argparse
import mysql.connector
from config import API_CONFIG, LOGGING_CONFIG, DATABASE_CONFIG

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

def setup_database():
    """
    Initialize database connection.
    
    Returns:
        bool: True if database connection successful
    """
    try:
        connection = mysql.connector.connect(**DATABASE_CONFIG)
        if connection.is_connected():
            logger.info("Database connection established successfully")
            connection.close()
            return True
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        return False

def create_directories():
    """Create necessary directories for logs and temporary files."""
    directories = ['logs', 'tmp']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f"Created directory: {directory}")

def main():
    """
    Main function to start the XBACnet API server.
    
    Parses command line arguments and starts the Gunicorn server
    with appropriate configuration.
    """
    parser = argparse.ArgumentParser(description='XBACnet API Server')
    parser.add_argument('--host', default=API_CONFIG['host'], 
                       help='Host to bind to (default: %(default)s)')
    parser.add_argument('--port', type=int, default=API_CONFIG['port'],
                       help='Port to bind to (default: %(default)s)')
    parser.add_argument('--workers', type=int, default=None,
                       help='Number of worker processes (default: auto)')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--reload', action='store_true',
                       help='Enable auto-reload on code changes')
    parser.add_argument('--log-level', default=LOGGING_CONFIG['level'],
                       choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                       help='Log level (default: %(default)s)')
    
    args = parser.parse_args()
    
    # Update logging level
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    # Create necessary directories
    create_directories()
    
    # Setup database connection
    if not setup_database():
        logger.error("Failed to setup database connection. Exiting.")
        sys.exit(1)
    
    # Prepare Gunicorn command
    cmd = [
        'gunicorn',
        '--config', 'gunicorn.conf.py',
        '--bind', f"{args.host}:{args.port}",
        '--log-level', args.log_level.lower()
    ]
    
    # Add optional arguments
    if args.workers:
        cmd.extend(['--workers', str(args.workers)])
    if args.debug:
        cmd.extend(['--reload'])
    if args.reload:
        cmd.extend(['--reload'])
        
    # Add application module
    cmd.append('app:app')
    
    logger.info(f"Starting XBACnet API server on {args.host}:{args.port}")
    logger.info(f"Command: {' '.join(cmd)}")
    
    # Start the server
    try:
        os.execvp('gunicorn', cmd)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

"""
XBACnet API Configuration

This module contains all configuration settings for the XBACnet REST API server.
It includes database connection settings, server configuration, and API parameters.

Author: XBACnet Team
Date: 2024
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database Configuration
DATABASE_CONFIG = {
    'host': os.getenv('XBACNET_DB_HOST', 'localhost'),
    'port': int(os.getenv('XBACNET_DB_PORT', '3306')),
    'user': os.getenv('XBACNET_DB_USER', 'root'),
    'password': os.getenv('XBACNET_DB_PASSWORD', ''),
    'database': os.getenv('XBACNET_DB_NAME', 'xbacnet'),
    'charset': 'utf8mb4',
    'autocommit': True,
    'time_zone': '+00:00'
}

# API Server Configuration
API_CONFIG = {
    'host': os.getenv('XBACNET_API_HOST', '0.0.0.0'),
    'port': int(os.getenv('XBACNET_API_PORT', '8000')),
    'debug': os.getenv('XBACNET_API_DEBUG', 'False').lower() == 'true'
}

# CORS Configuration
CORS_CONFIG = {
    'allow_origins': os.getenv('XBACNET_CORS_ORIGINS', '*').split(','),
    'allow_methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
    'max_age': 3600
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': os.getenv('XBACNET_LOG_LEVEL', 'INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': os.getenv('XBACNET_LOG_FILE', 'xbacnet-api.log')
}

# Pagination Configuration
PAGINATION_CONFIG = {
    'default_page_size': int(os.getenv('XBACNET_DEFAULT_PAGE_SIZE', '20')),
    'max_page_size': int(os.getenv('XBACNET_MAX_PAGE_SIZE', '100'))
}

# BACnet Object Configuration
BACNET_CONFIG = {
    'default_status_flags': '0000',  # IN_ALARM, FAULT, OVERRIDDEN, OUT_OF_SERVICE
    'default_event_state': 'normal',
    'default_out_of_service': False,
    'default_cov_increment': 1.0,
    'default_polarity': 'normal',
    'default_relinquish_default': 0.0
}

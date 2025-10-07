"""
XBACnet API Configuration

This module contains all configuration settings for the XBACnet REST API server.
It includes database connection settings, server configuration, and API parameters.

Author: XBACnet Team
Date: 2024
"""

from decouple import config

# Database Configuration
DATABASE_CONFIG = {
    'host': config('XBACNET_DB_HOST', default='localhost'),
    'port': config('XBACNET_DB_PORT', default=3306, cast=int),
    'user': config('XBACNET_DB_USER', default='root'),
    'password': config('XBACNET_DB_PASSWORD', default=''),
    'database': config('XBACNET_DB_NAME', default='xbacnet'),
    'charset': 'utf8mb4',
    'autocommit': True,
    'time_zone': '+00:00'
}

# API Server Configuration
API_CONFIG = {
    'host': config('XBACNET_API_HOST', default='0.0.0.0'),
    'port': config('XBACNET_API_PORT', default=8000, cast=int),
    'debug': config('XBACNET_API_DEBUG', default=False, cast=bool)
}

# CORS Configuration
CORS_CONFIG = {
    'allow_origins': config('XBACNET_CORS_ORIGINS', default='*').split(','),
    'allow_methods': ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    'allow_headers': ['Content-Type', 'Authorization', 'X-Requested-With'],
    'max_age': 3600
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': config('XBACNET_LOG_LEVEL', default='INFO'),
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': config('XBACNET_LOG_FILE', default='xbacnet-api.log')
}

# Pagination Configuration
PAGINATION_CONFIG = {
    'default_page_size': config('XBACNET_DEFAULT_PAGE_SIZE', default=20, cast=int),
    'max_page_size': config('XBACNET_MAX_PAGE_SIZE', default=100, cast=int)
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

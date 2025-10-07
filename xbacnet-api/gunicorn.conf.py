"""
Gunicorn Configuration for XBACnet API

This module contains the Gunicorn server configuration for the XBACnet REST API.
It defines server settings, worker processes, and performance parameters.

Author: XBACnet Team
Date: 2024
"""

import os
import multiprocessing
from config import API_CONFIG

# Server socket configuration
bind = f"{API_CONFIG['host']}:{API_CONFIG['port']}"
backlog = 2048

# Worker processes configuration
workers = multiprocessing.cpu_count() * 2 + 1  # Recommended formula
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Process naming
proc_name = 'xbacnet-api'

# Logging configuration
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process management
daemon = False
pidfile = 'logs/xbacnet-api.pid'
user = None
group = None
tmp_upload_dir = None

# Server mechanics
preload_app = True
reload = API_CONFIG['debug']
reload_engine = 'auto'

# SSL configuration (if needed)
# keyfile = '/path/to/keyfile'
# certfile = '/path/to/certfile'

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance tuning
worker_tmp_dir = '/dev/shm'  # Use shared memory for better performance

def when_ready(server):
    """
    Called just after the server is started.
    
    Args:
        server: Gunicorn server instance
    """
    server.log.info("XBACnet API server is ready to serve requests")

def worker_int(worker):
    """
    Called just after a worker has been interrupted.
    
    Args:
        worker: Gunicorn worker instance
    """
    worker.log.info("Worker received INT or QUIT signal")

def pre_fork(server, worker):
    """
    Called just before a worker is forked.
    
    Args:
        server: Gunicorn server instance
        worker: Gunicorn worker instance
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    
    Args:
        server: Gunicorn server instance
        worker: Gunicorn worker instance
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """
    Called just after a worker has initialized the application.
    
    Args:
        worker: Gunicorn worker instance
    """
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    """
    Called when a worker receives the SIGABRT signal.
    
    Args:
        worker: Gunicorn worker instance
    """
    worker.log.info("Worker aborted (pid: %s)", worker.pid)

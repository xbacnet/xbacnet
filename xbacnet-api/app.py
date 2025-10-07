"""
XBACnet API Main Application

This module creates the main Falcon application with all routes and middleware.
It sets up the REST API endpoints for managing BACnet objects and provides
CORS support for web applications.

Author: XBACnet Team
Date: 2024
"""

import falcon
import logging
from falcon_cors import CORS
from resources import (
    AnalogInputResource, AnalogOutputResource, AnalogValueResource,
    BinaryInputResource, BinaryOutputResource, BinaryValueResource,
    MultiStateInputResource, MultiStateOutputResource, MultiStateValueResource,
    HealthResource, StatsResource, UserResource, LoginResource, LogoutResource
)
from config import CORS_CONFIG, LOGGING_CONFIG

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOGGING_CONFIG['level']),
    format=LOGGING_CONFIG['format']
)
logger = logging.getLogger(__name__)

class RequireJSON:
    """
    Middleware to require JSON content type for POST and PUT requests.

    This middleware ensures that all POST and PUT requests have proper
    Content-Type headers and valid JSON bodies.
    """

    def process_request(self, req, resp):
        """
        Process incoming request to validate JSON content type.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        if req.method in ('POST', 'PUT'):
            if not req.content_type or 'application/json' not in req.content_type:
                raise falcon.HTTPBadRequest(
                    'Bad Request',
                    'Content-Type must be application/json'
                )


def create_app():
    """
    Create and configure the Falcon application.

    Returns:
        falcon.App: Configured Falcon application instance
    """
    # Configure CORS
    cors = CORS(
        allow_origins_list=CORS_CONFIG['allow_origins'],
        allow_methods_list=CORS_CONFIG['allow_methods'],
        allow_headers_list=CORS_CONFIG['allow_headers'],
        max_age=CORS_CONFIG['max_age']
    )

    # Create Falcon application with CORS middleware
    app = falcon.App(
        middleware=[
            cors.middleware,
            RequireJSON()
        ]
    )

    # Create resource instances
    analog_input_resource = AnalogInputResource()
    analog_output_resource = AnalogOutputResource()
    analog_value_resource = AnalogValueResource()
    binary_input_resource = BinaryInputResource()
    binary_output_resource = BinaryOutputResource()
    binary_value_resource = BinaryValueResource()
    multi_state_input_resource = MultiStateInputResource()
    multi_state_output_resource = MultiStateOutputResource()
    multi_state_value_resource = MultiStateValueResource()
    health_resource = HealthResource()
    stats_resource = StatsResource()
    user_resource = UserResource()
    login_resource = LoginResource()
    logout_resource = LogoutResource()

    # Add routes for analog objects
    app.add_route('/api/analog-inputs', analog_input_resource)
    app.add_route('/api/analog-inputs/{object_id:int}', analog_input_resource)

    app.add_route('/api/analog-outputs', analog_output_resource)
    app.add_route('/api/analog-outputs/{object_id:int}', analog_output_resource)

    app.add_route('/api/analog-values', analog_value_resource)
    app.add_route('/api/analog-values/{object_id:int}', analog_value_resource)

    # Add routes for binary objects
    app.add_route('/api/binary-inputs', binary_input_resource)
    app.add_route('/api/binary-inputs/{object_id:int}', binary_input_resource)

    app.add_route('/api/binary-outputs', binary_output_resource)
    app.add_route('/api/binary-outputs/{object_id:int}', binary_output_resource)

    app.add_route('/api/binary-values', binary_value_resource)
    app.add_route('/api/binary-values/{object_id:int}', binary_value_resource)

    # Add routes for multi-state objects
    app.add_route('/api/multi-state-inputs', multi_state_input_resource)
    app.add_route('/api/multi-state-inputs/{object_id:int}', multi_state_input_resource)

    app.add_route('/api/multi-state-outputs', multi_state_output_resource)
    app.add_route('/api/multi-state-outputs/{object_id:int}', multi_state_output_resource)

    app.add_route('/api/multi-state-values', multi_state_value_resource)
    app.add_route('/api/multi-state-values/{object_id:int}', multi_state_value_resource)

    # Add utility routes
    app.add_route('/api/health', health_resource)
    app.add_route('/api/stats', stats_resource)

    # Add user management routes
    app.add_route('/api/users', user_resource)
    app.add_route('/api/users/{user_id:int}', user_resource)
    app.add_route('/api/login', login_resource)
    app.add_route('/api/logout', logout_resource)

    # Add root endpoint with API information
    app.add_route('/', RootResource())

    logger.info("XBACnet API application created successfully")
    return app

class RootResource:
    """
    Root resource that provides API information and documentation.
    """

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle GET requests to root endpoint.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        resp.media = {
            'name': 'XBACnet API',
            'version': '1.0.0',
            'description': 'REST API for managing BACnet objects',
            'endpoints': {
                'analog_inputs': '/api/analog-inputs',
                'analog_outputs': '/api/analog-outputs',
                'analog_values': '/api/analog-values',
                'binary_inputs': '/api/binary-inputs',
                'binary_outputs': '/api/binary-outputs',
                'binary_values': '/api/binary-values',
                'multi_state_inputs': '/api/multi-state-inputs',
                'multi_state_outputs': '/api/multi-state-outputs',
                'multi_state_values': '/api/multi-state-values',
                'users': '/api/users',
                'login': '/api/login',
                'logout': '/api/logout',
                'health': '/api/health',
                'stats': '/api/stats'
            },
            'documentation': 'https://github.com/xbacnet/xbacnet-api'
        }
        resp.status = falcon.HTTP_200

# Create the application instance
app = create_app()

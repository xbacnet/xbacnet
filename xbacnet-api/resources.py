"""
XBACnet API Resources

This module defines Falcon API resources for managing BACnet objects.
Each resource handles HTTP methods (GET, POST, PUT, DELETE) for specific
BACnet object types and provides RESTful API endpoints.

Author: XBACnet Team
Date: 2024
"""

import falcon
import json
import logging
from datetime import datetime
from typing import Dict, Any
from models import MODELS
from config import PAGINATION_CONFIG

# Configure logger
logger = logging.getLogger(__name__)

class BaseResource:
    """
    Base resource class for all BACnet object types.

    Provides common HTTP method implementations and error handling.
    """

    def __init__(self, model_name: str):
        """
        Initialize base resource.

        Args:
            model_name (str): Name of the model to use
        """
        self.model = MODELS[model_name]
        self.model_name = model_name

    def on_get(self, req: falcon.Request, resp: falcon.Response, object_id: int = None):
        """
        Handle GET requests.

        Args:
            req: Falcon request object
            resp: Falcon response object
            object_id: Optional object ID for single object retrieval
        """
        try:
            if object_id:
                # Get single object by ID
                result = self.model.get_by_id(object_id)
                if result:
                    resp.media = result
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_404
                    resp.media = {'error': f'{self.model_name} with ID {object_id} not found'}
            else:
                # Get paginated list of objects
                page = int(req.get_param('page', default=1))
                page_size = int(req.get_param('page_size', default=PAGINATION_CONFIG['default_page_size']))

                # Validate pagination parameters
                if page < 1:
                    page = 1
                if page_size > PAGINATION_CONFIG['max_page_size']:
                    page_size = PAGINATION_CONFIG['max_page_size']

                result = self.model.get_all(page, page_size)
                resp.media = result
                resp.status = falcon.HTTP_200

        except Exception as e:
            logger.error(f"Error in GET {self.model_name}: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle POST requests for creating new objects.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Create new object
            object_id = self.model.create(data)

            # Return created object
            result = self.model.get_by_id(object_id)
            resp.media = result
            resp.status = falcon.HTTP_201

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in POST {self.model_name}: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_put(self, req: falcon.Request, resp: falcon.Response, object_id: int):
        """
        Handle PUT requests for updating existing objects.

        Args:
            req: Falcon request object
            resp: Falcon response object
            object_id: Object ID to update
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Update object
            success = self.model.update(object_id, data)

            if success:
                # Return updated object
                result = self.model.get_by_id(object_id)
                resp.media = result
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': f'{self.model_name} with ID {object_id} not found'}

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in PUT {self.model_name}: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_delete(self, req: falcon.Request, resp: falcon.Response, object_id: int):
        """
        Handle DELETE requests for removing objects.

        Args:
            req: Falcon request object
            resp: Falcon response object
            object_id: Object ID to delete
        """
        try:
            # Delete object
            success = self.model.delete(object_id)

            if success:
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': f'{self.model_name} with ID {object_id} not found'}

        except Exception as e:
            logger.error(f"Error in DELETE {self.model_name}: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

# Resource classes for each BACnet object type
class AnalogInputResource(BaseResource):
    """Resource for managing analog input objects."""
    def __init__(self):
        super().__init__('analog_input')

class AnalogOutputResource(BaseResource):
    """Resource for managing analog output objects."""
    def __init__(self):
        super().__init__('analog_output')

class AnalogValueResource(BaseResource):
    """Resource for managing analog value objects."""
    def __init__(self):
        super().__init__('analog_value')

class BinaryInputResource(BaseResource):
    """Resource for managing binary input objects."""
    def __init__(self):
        super().__init__('binary_input')

class BinaryOutputResource(BaseResource):
    """Resource for managing binary output objects."""
    def __init__(self):
        super().__init__('binary_output')

class BinaryValueResource(BaseResource):
    """Resource for managing binary value objects."""
    def __init__(self):
        super().__init__('binary_value')

class MultiStateInputResource(BaseResource):
    """Resource for managing multi-state input objects."""
    def __init__(self):
        super().__init__('multi_state_input')

class MultiStateOutputResource(BaseResource):
    """Resource for managing multi-state output objects."""
    def __init__(self):
        super().__init__('multi_state_output')

class MultiStateValueResource(BaseResource):
    """Resource for managing multi-state value objects."""
    def __init__(self):
        super().__init__('multi_state_value')

class HealthResource:
    """
    Health check resource for API monitoring.

    Provides endpoint to check API and database connectivity status.
    """

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle health check requests.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            import mysql.connector
            from config import DATABASE_CONFIG

            # Check database connectivity
            try:
                connection = mysql.connector.connect(**DATABASE_CONFIG)
                db_status = "connected"
                connection.close()
            except:
                db_status = "disconnected"

            resp.media = {
                'status': 'healthy',
                'database': db_status,
                'timestamp': datetime.utcnow().isoformat()
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            logger.error(f"Health check error: {e}")
            resp.status = falcon.HTTP_503
            resp.media = {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }

class StatsResource:
    """
    Statistics resource for API usage monitoring.

    Provides endpoint to get statistics about BACnet objects in the database.
    """

    def on_get(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle statistics requests.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            import mysql.connector
            from config import DATABASE_CONFIG

            stats = {}
            connection = None
            cursor = None

            try:
                connection = mysql.connector.connect(**DATABASE_CONFIG)
                cursor = connection.cursor(dictionary=True)

                # Get count for each object type
                for model_name, model in MODELS.items():
                    if hasattr(model, 'table_name'):
                        count_query = f"SELECT COUNT(*) as count FROM {model.table_name}"
                        cursor.execute(count_query)
                        result = cursor.fetchone()
                        stats[model_name] = result['count'] if result else 0

            finally:
                if cursor:
                    cursor.close()
                if connection and connection.is_connected():
                    connection.close()

            resp.media = {
                'object_counts': stats,
                'timestamp': datetime.utcnow().isoformat()
            }
            resp.status = falcon.HTTP_200

        except Exception as e:
            logger.error(f"Stats error: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

class UserResource:
    """
    User management resource for handling user operations.

    Provides endpoints for user CRUD operations and authentication.
    """

    def __init__(self):
        """Initialize user resource."""
        self.model = MODELS['user']

    def on_get(self, req: falcon.Request, resp: falcon.Response, user_id: int = None):
        """
        Handle GET requests for users.

        Args:
            req: Falcon request object
            resp: Falcon response object
            user_id: Optional user ID for single user retrieval
        """
        try:
            if user_id:
                # Get single user by ID
                result = self.model.get_by_id(user_id)
                if result:
                    resp.media = result
                    resp.status = falcon.HTTP_200
                else:
                    resp.status = falcon.HTTP_404
                    resp.media = {'error': f'User with ID {user_id} not found'}
            else:
                # Get paginated list of users
                page = int(req.get_param('page', default=1))
                page_size = int(req.get_param('page_size', default=PAGINATION_CONFIG['default_page_size']))

                # Validate pagination parameters
                if page < 1:
                    page = 1
                if page_size > PAGINATION_CONFIG['max_page_size']:
                    page_size = PAGINATION_CONFIG['max_page_size']

                result = self.model.get_all(page, page_size)
                resp.media = result
                resp.status = falcon.HTTP_200

        except Exception as e:
            logger.error(f"Error in GET users: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle POST requests for creating new users.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Create new user
            user_id = self.model.create(data)

            # Return created user
            result = self.model.get_by_id(user_id)
            resp.media = result
            resp.status = falcon.HTTP_201

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in POST users: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_put(self, req: falcon.Request, resp: falcon.Response, user_id: int):
        """
        Handle PUT requests for updating existing users.

        Args:
            req: Falcon request object
            resp: Falcon response object
            user_id: User ID to update
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Update user
            success = self.model.update(user_id, data)

            if success:
                # Return updated user
                result = self.model.get_by_id(user_id)
                resp.media = result
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': f'User with ID {user_id} not found'}

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in PUT users: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

    def on_delete(self, req: falcon.Request, resp: falcon.Response, user_id: int):
        """
        Handle DELETE requests for removing users.

        Args:
            req: Falcon request object
            resp: Falcon response object
            user_id: User ID to delete
        """
        try:
            # Delete user
            success = self.model.delete(user_id)

            if success:
                resp.status = falcon.HTTP_204
            else:
                resp.status = falcon.HTTP_404
                resp.media = {'error': f'User with ID {user_id} not found'}

        except Exception as e:
            logger.error(f"Error in DELETE users: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

class LoginResource:
    """
    User authentication resource for handling login operations.

    Provides endpoint for user authentication and login.
    """

    def __init__(self):
        """Initialize login resource."""
        self.model = MODELS['user']

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle POST requests for user authentication.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Validate login data
            validated_data = self.model.validate_login_data(data)

            # Authenticate user
            user = self.model.authenticate(validated_data['name'], validated_data['password'])

            if user:
                resp.media = {
                    'success': True,
                    'user': user,
                    'message': 'Login successful'
                }
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_401
                resp.media = {
                    'success': False,
                    'error': 'Invalid username or password'
                }

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in POST login: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

class LogoutResource:
    """
    User logout resource for handling logout operations.

    Provides endpoint for user logout and session termination.
    """

    def __init__(self):
        """Initialize logout resource."""
        self.model = MODELS['user']

    def on_post(self, req: falcon.Request, resp: falcon.Response):
        """
        Handle POST requests for user logout.

        Args:
            req: Falcon request object
            resp: Falcon response object
        """
        try:
            # Parse request body
            data = json.loads(req.bounded_stream.read().decode('utf-8'))

            # Validate logout data
            validated_data = self.model.validate_logout_data(data)

            # Logout user
            success = False
            if 'user_id' in validated_data:
                success = self.model.logout(user_id=validated_data['user_id'])
            elif 'name' in validated_data:
                success = self.model.logout(name=validated_data['name'])

            if success:
                resp.media = {
                    'success': True,
                    'message': 'Logout successful'
                }
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
                resp.media = {
                    'success': False,
                    'error': 'User not found'
                }

        except json.JSONDecodeError:
            resp.status = falcon.HTTP_400
            resp.media = {'error': 'Invalid JSON in request body'}
        except Exception as e:
            logger.error(f"Error in POST logout: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {'error': 'Internal server error'}

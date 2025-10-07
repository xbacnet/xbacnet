"""
XBACnet API Database Models

This module defines data models and validation schemas for all BACnet object types.
It provides structured access to database tables and ensures data consistency.

Author: XBACnet Team
Date: 2024
"""

import jsonschema
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from typing import Dict, List, Optional, Any
from config import DATABASE_CONFIG
import logging

# Configure logger
logger = logging.getLogger(__name__)

# JSON Schemas for validation
ANALOG_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "number"},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal", "highLimit", "lowLimit"]},
        "out_of_service": {"type": "boolean"},
        "units": {"type": "string", "maxLength": 255},
        "cov_increment": {"type": "number", "minimum": 0}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "units"]
}

ANALOG_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "number"},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal", "highLimit", "lowLimit"]},
        "out_of_service": {"type": "boolean"},
        "units": {"type": "string", "maxLength": 255},
        "relinquish_default": {"type": "number"},
        "current_command_priority": {"type": "integer", "minimum": 1, "maximum": 16},
        "cov_increment": {"type": "number", "minimum": 0}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "units", "relinquish_default"]
}

BINARY_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "string", "enum": ["active", "inactive"]},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal"]},
        "out_of_service": {"type": "boolean"},
        "polarity": {"type": "string", "enum": ["normal", "reverse"]}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "polarity"]
}

BINARY_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "string", "enum": ["active", "inactive"]},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal"]},
        "out_of_service": {"type": "boolean"},
        "polarity": {"type": "string", "enum": ["normal", "reverse"]},
        "relinquish_default": {"type": "string", "enum": ["active", "inactive"]},
        "current_command_priority": {"type": "integer", "minimum": 1, "maximum": 16}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "polarity", "relinquish_default"]
}

MULTI_STATE_INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "integer", "minimum": 1},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal"]},
        "out_of_service": {"type": "boolean"},
        "number_of_states": {"type": "integer", "minimum": 1, "maximum": 255},
        "state_text": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "number_of_states"]
}

MULTI_STATE_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "object_identifier": {"type": "integer", "minimum": 1},
        "object_name": {"type": "string", "minLength": 1, "maxLength": 255},
        "present_value": {"type": "integer", "minimum": 1},
        "description": {"type": "string", "maxLength": 255},
        "status_flags": {"type": "string", "pattern": "^[01]{4}$"},
        "event_state": {"type": "string", "enum": ["normal", "fault", "offnormal"]},
        "out_of_service": {"type": "boolean"},
        "number_of_states": {"type": "integer", "minimum": 1, "maximum": 255},
        "state_text": {"type": "array", "items": {"type": "string"}},
        "relinquish_default": {"type": "integer", "minimum": 1},
        "current_command_priority": {"type": "integer", "minimum": 1, "maximum": 16}
    },
    "required": ["object_identifier", "object_name", "present_value", "status_flags",
                "event_state", "out_of_service", "number_of_states", "relinquish_default"]
}

# User management schemas
USER_CREATE_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 128},
        "display_name": {"type": "string", "minLength": 1, "maxLength": 128},
        "email": {"type": "string", "format": "email", "maxLength": 128},
        "password": {"type": "string", "minLength": 6, "maxLength": 128},
        "is_admin": {"type": "boolean"}
    },
    "required": ["name", "display_name", "email", "password"]
}

USER_UPDATE_SCHEMA = {
    "type": "object",
    "properties": {
        "display_name": {"type": "string", "minLength": 1, "maxLength": 128},
        "email": {"type": "string", "format": "email", "maxLength": 128},
        "password": {"type": "string", "minLength": 6, "maxLength": 128},
        "is_admin": {"type": "boolean"}
    }
}

USER_LOGIN_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1, "maxLength": 128},
        "password": {"type": "string", "minLength": 1, "maxLength": 128}
    },
    "required": ["name", "password"]
}

USER_LOGOUT_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {"type": "integer", "minimum": 1},
        "name": {"type": "string", "minLength": 1, "maxLength": 128}
    }
}

class BaseModel:
    """
    Base model class for all BACnet objects.

    Provides common functionality for database operations and data validation.
    """

    def __init__(self, table_name: str, schema: Dict):
        """
        Initialize base model.

        Args:
            table_name (str): Database table name
            schema (dict): JSON schema for validation
        """
        self.table_name = table_name
        self.schema = schema

    def _get_connection(self):
        """
        Get database connection.

        Returns:
            mysql.connector.connection: Database connection object
        """
        try:
            connection = mysql.connector.connect(**DATABASE_CONFIG)
            return connection
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def validate_data(self, data: Dict) -> Dict:
        """
        Validate data against JSON schema.

        Args:
            data (dict): Data to validate

        Returns:
            dict: Validated data

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(data, self.schema)
            return data
        except jsonschema.ValidationError as e:
            logger.error(f"Data validation error: {e}")
            raise

    def get_all(self, page: int = 1, page_size: int = 20) -> Dict:
        """
        Get all objects with pagination.

        Args:
            page (int): Page number (1-based)
            page_size (int): Number of items per page

        Returns:
            dict: Paginated results with metadata
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            offset = (page - 1) * page_size

            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM {self.table_name}"
            cursor.execute(count_query)
            total_result = cursor.fetchone()
            total = total_result['total'] if total_result else 0

            # Get paginated data
            data_query = f"SELECT * FROM {self.table_name} ORDER BY id LIMIT %s OFFSET %s"
            cursor.execute(data_query, (page_size, offset))
            data = cursor.fetchall()

            return {
                'data': data or [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'pages': (total + page_size - 1) // page_size
                }
            }
        except Error as e:
            logger.error(f"Error in get_all: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_by_id(self, object_id: int) -> Optional[Dict]:
        """
        Get object by ID.

        Args:
            object_id (int): Object ID

        Returns:
            dict or None: Object data if found
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE id = %s"
            cursor.execute(query, (object_id,))
            return cursor.fetchone()
        except Error as e:
            logger.error(f"Error in get_by_id: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_by_identifier(self, object_identifier: int) -> Optional[Dict]:
        """
        Get object by BACnet object identifier.

        Args:
            object_identifier (int): BACnet object identifier

        Returns:
            dict or None: Object data if found
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE object_identifier = %s"
            cursor.execute(query, (object_identifier,))
            return cursor.fetchone()
        except Error as e:
            logger.error(f"Error in get_by_identifier: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def create(self, data: Dict) -> int:
        """
        Create new object.

        Args:
            data (dict): Object data

        Returns:
            int: ID of created object
        """
        connection = None
        cursor = None
        try:
            validated_data = self.validate_data(data)
            connection = self._get_connection()
            cursor = connection.cursor()

            # Build INSERT query
            columns = list(validated_data.keys())
            placeholders = ', '.join(['%s'] * len(columns))
            values = list(validated_data.values())

            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Error in create: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def update(self, object_id: int, data: Dict) -> bool:
        """
        Update existing object.

        Args:
            object_id (int): Object ID
            data (dict): Updated data

        Returns:
            bool: True if update successful
        """
        connection = None
        cursor = None
        try:
            validated_data = self.validate_data(data)
            connection = self._get_connection()
            cursor = connection.cursor()

            # Build UPDATE query
            set_clauses = [f"{key} = %s" for key in validated_data.keys()]
            values = list(validated_data.values()) + [object_id]

            query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = %s"
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error in update: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def delete(self, object_id: int) -> bool:
        """
        Delete object by ID.

        Args:
            object_id (int): Object ID

        Returns:
            bool: True if deletion successful
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id = %s"
            cursor.execute(query, (object_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error in delete: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

class UserModel:
    """
    User management model for handling user operations.

    Provides functionality for user creation, authentication, and management.
    """

    def __init__(self):
        """Initialize user model."""
        self.table_name = 'tbl_users'

    def _get_connection(self):
        """
        Get database connection.

        Returns:
            mysql.connector.connection: Database connection object
        """
        try:
            connection = mysql.connector.connect(**DATABASE_CONFIG)
            return connection
        except Error as e:
            logger.error(f"Error connecting to MySQL database: {e}")
            raise

    def _generate_uuid(self):
        """Generate a UUID for new users."""
        import uuid
        return str(uuid.uuid4())

    def _generate_salt(self):
        """Generate a salt for password hashing."""
        import hashlib
        import secrets
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

    def _hash_password(self, password: str, salt: str) -> str:
        """
        Hash password with salt.

        Args:
            password (str): Plain text password
            salt (str): Salt for hashing

        Returns:
            str: Hashed password
        """
        import hashlib
        return hashlib.sha512((password + salt).encode()).hexdigest()

    def validate_create_data(self, data: Dict) -> Dict:
        """
        Validate user creation data.

        Args:
            data (dict): User data to validate

        Returns:
            dict: Validated data

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(data, USER_CREATE_SCHEMA)
            return data
        except jsonschema.ValidationError as e:
            logger.error(f"User creation data validation error: {e}")
            raise

    def validate_update_data(self, data: Dict) -> Dict:
        """
        Validate user update data.

        Args:
            data (dict): User data to validate

        Returns:
            dict: Validated data

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(data, USER_UPDATE_SCHEMA)
            return data
        except jsonschema.ValidationError as e:
            logger.error(f"User update data validation error: {e}")
            raise

    def validate_login_data(self, data: Dict) -> Dict:
        """
        Validate user login data.

        Args:
            data (dict): Login data to validate

        Returns:
            dict: Validated data

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(data, USER_LOGIN_SCHEMA)
            return data
        except jsonschema.ValidationError as e:
            logger.error(f"User login data validation error: {e}")
            raise

    def validate_logout_data(self, data: Dict) -> Dict:
        """
        Validate user logout data.

        Args:
            data (dict): Logout data to validate

        Returns:
            dict: Validated data

        Raises:
            jsonschema.ValidationError: If validation fails
        """
        try:
            jsonschema.validate(data, USER_LOGOUT_SCHEMA)
            return data
        except jsonschema.ValidationError as e:
            logger.error(f"User logout data validation error: {e}")
            raise

    def get_all(self, page: int = 1, page_size: int = 20) -> Dict:
        """
        Get all users with pagination.

        Args:
            page (int): Page number (1-based)
            page_size (int): Number of items per page

        Returns:
            dict: Paginated results with metadata
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            offset = (page - 1) * page_size

            # Get total count
            count_query = f"SELECT COUNT(*) as total FROM {self.table_name}"
            cursor.execute(count_query)
            total_result = cursor.fetchone()
            total = total_result['total'] if total_result else 0

            # Get paginated data (exclude password and salt)
            data_query = f"SELECT id, name, uuid, display_name, email, is_admin FROM {self.table_name} ORDER BY id LIMIT %s OFFSET %s"
            cursor.execute(data_query, (page_size, offset))
            data = cursor.fetchall()

            return {
                'data': data or [],
                'pagination': {
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'pages': (total + page_size - 1) // page_size
                }
            }
        except Error as e:
            logger.error(f"Error in get_all: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Get user by ID.

        Args:
            user_id (int): User ID

        Returns:
            dict or None: User data if found (without password and salt)
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT id, name, uuid, display_name, email, is_admin FROM {self.table_name} WHERE id = %s"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        except Error as e:
            logger.error(f"Error in get_by_id: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def get_by_name(self, name: str) -> Optional[Dict]:
        """
        Get user by name.

        Args:
            name (str): Username

        Returns:
            dict or None: User data if found (without password and salt)
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)
            query = f"SELECT id, name, uuid, display_name, email, is_admin FROM {self.table_name} WHERE name = %s"
            cursor.execute(query, (name,))
            return cursor.fetchone()
        except Error as e:
            logger.error(f"Error in get_by_name: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def create(self, data: Dict) -> int:
        """
        Create new user.

        Args:
            data (dict): User data

        Returns:
            int: ID of created user
        """
        connection = None
        cursor = None
        try:
            validated_data = self.validate_create_data(data)
            connection = self._get_connection()
            cursor = connection.cursor()

            # Generate UUID and salt
            uuid = self._generate_uuid()
            salt = self._generate_salt()
            hashed_password = self._hash_password(validated_data['password'], salt)

            # Prepare data for insertion
            insert_data = {
                'name': validated_data['name'],
                'uuid': uuid,
                'display_name': validated_data['display_name'],
                'email': validated_data['email'],
                'salt': salt,
                'password': hashed_password,
                'is_admin': validated_data.get('is_admin', False)
            }

            # Build INSERT query
            columns = list(insert_data.keys())
            placeholders = ', '.join(['%s'] * len(columns))
            values = list(insert_data.values())

            query = f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            connection.commit()
            return cursor.lastrowid
        except Error as e:
            logger.error(f"Error in create: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def update(self, user_id: int, data: Dict) -> bool:
        """
        Update existing user.

        Args:
            user_id (int): User ID
            data (dict): Updated data

        Returns:
            bool: True if update successful
        """
        connection = None
        cursor = None
        try:
            validated_data = self.validate_update_data(data)
            connection = self._get_connection()
            cursor = connection.cursor()

            # Prepare update data
            update_data = {}
            for key, value in validated_data.items():
                if key == 'password':
                    # Hash new password
                    salt = self._generate_salt()
                    hashed_password = self._hash_password(value, salt)
                    update_data['password'] = hashed_password
                    update_data['salt'] = salt
                else:
                    update_data[key] = value

            if not update_data:
                return False

            # Build UPDATE query
            set_clauses = [f"{key} = %s" for key in update_data.keys()]
            values = list(update_data.values()) + [user_id]

            query = f"UPDATE {self.table_name} SET {', '.join(set_clauses)} WHERE id = %s"
            cursor.execute(query, values)
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error in update: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def delete(self, user_id: int) -> bool:
        """
        Delete user by ID.

        Args:
            user_id (int): User ID

        Returns:
            bool: True if deletion successful
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            return cursor.rowcount > 0
        except Error as e:
            logger.error(f"Error in delete: {e}")
            if connection:
                connection.rollback()
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def authenticate(self, name: str, password: str) -> Optional[Dict]:
        """
        Authenticate user with name and password.

        Args:
            name (str): Username
            password (str): Plain text password

        Returns:
            dict or None: User data if authentication successful (without password and salt)
        """
        connection = None
        cursor = None
        try:
            connection = self._get_connection()
            cursor = connection.cursor(dictionary=True)

            # Get user with password and salt
            query = f"SELECT id, name, uuid, display_name, email, salt, password, is_admin FROM {self.table_name} WHERE name = %s"
            cursor.execute(query, (name,))
            user = cursor.fetchone()

            if not user:
                return None

            # Verify password
            hashed_password = self._hash_password(password, user['salt'])
            if hashed_password != user['password']:
                return None

            # Return user data without password and salt
            return {
                'id': user['id'],
                'name': user['name'],
                'uuid': user['uuid'],
                'display_name': user['display_name'],
                'email': user['email'],
                'is_admin': user['is_admin']
            }
        except Error as e:
            logger.error(f"Error in authenticate: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection and connection.is_connected():
                connection.close()

    def logout(self, user_id: int = None, name: str = None) -> bool:
        """
        Logout user by ID or name.

        Args:
            user_id (int, optional): User ID
            name (str, optional): Username

        Returns:
            bool: True if logout successful
        """
        try:
            # For now, logout is just a validation that the user exists
            # In a real implementation, you might want to:
            # - Invalidate JWT tokens
            # - Clear session data
            # - Log the logout event

            if user_id:
                user = self.get_by_id(user_id)
                if user:
                    logger.info(f"User {user['name']} (ID: {user_id}) logged out")
                    return True
            elif name:
                user = self.get_by_name(name)
                if user:
                    logger.info(f"User {name} (ID: {user['id']}) logged out")
                    return True

            return False
        except Exception as e:
            logger.error(f"Error in logout: {e}")
            return False

# Model instances for each BACnet object type
AnalogInputModel = BaseModel('tbl_analog_input_objects', ANALOG_INPUT_SCHEMA)
AnalogOutputModel = BaseModel('tbl_analog_output_objects', ANALOG_OUTPUT_SCHEMA)
AnalogValueModel = BaseModel('tbl_analog_value_objects', ANALOG_INPUT_SCHEMA)  # Same schema as input
BinaryInputModel = BaseModel('tbl_binary_input_objects', BINARY_INPUT_SCHEMA)
BinaryOutputModel = BaseModel('tbl_binary_output_objects', BINARY_OUTPUT_SCHEMA)
BinaryValueModel = BaseModel('tbl_binary_value_objects', BINARY_INPUT_SCHEMA)  # Same schema as input
MultiStateInputModel = BaseModel('tbl_multi_state_input_objects', MULTI_STATE_INPUT_SCHEMA)
MultiStateOutputModel = BaseModel('tbl_multi_state_output_objects', MULTI_STATE_OUTPUT_SCHEMA)
MultiStateValueModel = BaseModel('tbl_multi_state_value_objects', MULTI_STATE_INPUT_SCHEMA)  # Same schema as input

# User model instance
UserModel = UserModel()

# Model registry for easy access
MODELS = {
    'analog_input': AnalogInputModel,
    'analog_output': AnalogOutputModel,
    'analog_value': AnalogValueModel,
    'binary_input': BinaryInputModel,
    'binary_output': BinaryOutputModel,
    'binary_value': BinaryValueModel,
    'multi_state_input': MultiStateInputModel,
    'multi_state_output': MultiStateOutputModel,
    'multi_state_value': MultiStateValueModel,
    'user': UserModel
}

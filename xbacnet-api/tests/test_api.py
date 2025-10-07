"""
XBACnet API Tests

This module contains unit tests for the XBACnet REST API.
It tests all endpoints and functionality to ensure proper operation.

Author: XBACnet Team
Date: 2024
"""

import pytest
import json
from falcon import testing
from app import app

class TestXBACnetAPI:
    """
    Test class for XBACnet API endpoints.

    This class contains tests for all API endpoints and functionality.
    """

    @pytest.fixture
    def client(self):
        """
        Create a test client for the API.

        Returns:
            falcon.testing.TestClient: Test client instance
        """
        return testing.TestClient(app)

    def test_root_endpoint(self, client):
        """Test the root endpoint returns API information."""
        result = client.simulate_get('/')
        assert result.status_code == 200

        data = json.loads(result.content)
        assert data['name'] == 'XBACnet API'
        assert data['version'] == '1.0.0'
        assert 'endpoints' in data

    def test_health_endpoint(self, client):
        """Test the health check endpoint."""
        result = client.simulate_get('/api/health')
        assert result.status_code == 200

        data = json.loads(result.content)
        assert 'status' in data
        assert 'timestamp' in data

    def test_stats_endpoint(self, client):
        """Test the statistics endpoint."""
        result = client.simulate_get('/api/stats')
        assert result.status_code == 200

        data = json.loads(result.content)
        assert 'object_counts' in data
        assert 'timestamp' in data

    def test_analog_input_crud(self, client):
        """Test CRUD operations for analog input objects."""
        # Test data
        test_data = {
            "object_identifier": 10001,
            "object_name": "Test_Analog_Input",
            "present_value": 25.5,
            "description": "Test analog input",
            "status_flags": "0000",
            "event_state": "normal",
            "out_of_service": False,
            "units": "degreesCelsius",
            "cov_increment": 0.1
        }

        # Create object
        result = client.simulate_post(
            '/api/analog-inputs',
            body=json.dumps(test_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 201

        created_data = json.loads(result.content)
        object_id = created_data['id']

        # Get object by ID
        result = client.simulate_get(f'/api/analog-inputs/{object_id}')
        assert result.status_code == 200

        # Update object
        update_data = {"present_value": 26.0}
        result = client.simulate_put(
            f'/api/analog-inputs/{object_id}',
            body=json.dumps(update_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 200

        # Delete object
        result = client.simulate_delete(f'/api/analog-inputs/{object_id}')
        assert result.status_code == 204

        # Verify deletion
        result = client.simulate_get(f'/api/analog-inputs/{object_id}')
        assert result.status_code == 404

    def test_binary_input_crud(self, client):
        """Test CRUD operations for binary input objects."""
        # Test data
        test_data = {
            "object_identifier": 40001,
            "object_name": "Test_Binary_Input",
            "present_value": "active",
            "description": "Test binary input",
            "status_flags": "0000",
            "event_state": "normal",
            "out_of_service": False,
            "polarity": "normal"
        }

        # Create object
        result = client.simulate_post(
            '/api/binary-inputs',
            body=json.dumps(test_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 201

        created_data = json.loads(result.content)
        object_id = created_data['id']

        # Get object by ID
        result = client.simulate_get(f'/api/binary-inputs/{object_id}')
        assert result.status_code == 200

        # Update object
        update_data = {"present_value": "inactive"}
        result = client.simulate_put(
            f'/api/binary-inputs/{object_id}',
            body=json.dumps(update_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 200

        # Delete object
        result = client.simulate_delete(f'/api/binary-inputs/{object_id}')
        assert result.status_code == 204

    def test_multi_state_input_crud(self, client):
        """Test CRUD operations for multi-state input objects."""
        # Test data
        test_data = {
            "object_identifier": 70001,
            "object_name": "Test_Multi_State_Input",
            "present_value": 1,
            "description": "Test multi-state input",
            "status_flags": "0000",
            "event_state": "normal",
            "out_of_service": False,
            "number_of_states": 3,
            "state_text": ["Off", "On", "Auto"]
        }

        # Create object
        result = client.simulate_post(
            '/api/multi-state-inputs',
            body=json.dumps(test_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 201

        created_data = json.loads(result.content)
        object_id = created_data['id']

        # Get object by ID
        result = client.simulate_get(f'/api/multi-state-inputs/{object_id}')
        assert result.status_code == 200

        # Update object
        update_data = {"present_value": 2}
        result = client.simulate_put(
            f'/api/multi-state-inputs/{object_id}',
            body=json.dumps(update_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 200

        # Delete object
        result = client.simulate_delete(f'/api/multi-state-inputs/{object_id}')
        assert result.status_code == 204

    def test_pagination(self, client):
        """Test pagination functionality."""
        result = client.simulate_get('/api/analog-inputs?page=1&page_size=5')
        assert result.status_code == 200

        data = json.loads(result.content)
        assert 'data' in data
        assert 'pagination' in data
        assert data['pagination']['page'] == 1
        assert data['pagination']['page_size'] == 5

    def test_invalid_json(self, client):
        """Test handling of invalid JSON in request body."""
        result = client.simulate_post(
            '/api/analog-inputs',
            body='invalid json',
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 400

    def test_validation_error(self, client):
        """Test data validation errors."""
        invalid_data = {
            "object_identifier": "invalid",  # Should be integer
            "object_name": "",  # Should not be empty
            "present_value": 25.5
        }

        result = client.simulate_post(
            '/api/analog-inputs',
            body=json.dumps(invalid_data),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 500  # Validation error

    def test_not_found(self, client):
        """Test 404 responses for non-existent objects."""
        result = client.simulate_get('/api/analog-inputs/99999')
        assert result.status_code == 404

        result = client.simulate_put(
            '/api/analog-inputs/99999',
            body=json.dumps({"present_value": 25.0}),
            headers={'Content-Type': 'application/json'}
        )
        assert result.status_code == 404

        result = client.simulate_delete('/api/analog-inputs/99999')
        assert result.status_code == 404

#!/usr/bin/env python3
"""
XBACnet API Usage Examples

This script demonstrates how to use the XBACnet REST API to manage BACnet objects.
It provides examples for creating, reading, updating, and deleting various object types.

Author: XBACnet Team
Date: 2024
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000/api"

def print_response(response, title):
    """Print formatted API response."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Status Code: {response.status_code}")
    if response.content:
        try:
            data = response.json()
            print(f"Response: {json.dumps(data, indent=2)}")
        except:
            print(f"Response: {response.text}")
    print(f"{'='*50}")

def test_health_check():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def test_api_info():
    """Test the root API endpoint."""
    response = requests.get("http://localhost:8000/")
    print_response(response, "API Information")

def test_stats():
    """Test the statistics endpoint."""
    response = requests.get(f"{BASE_URL}/stats")
    print_response(response, "Statistics")

def create_analog_input():
    """Create an analog input object."""
    data = {
        "object_identifier": 10001,
        "object_name": "Temperature_Sensor_1",
        "present_value": 25.5,
        "description": "Room temperature sensor",
        "status_flags": "0000",
        "event_state": "normal",
        "out_of_service": False,
        "units": "degreesCelsius",
        "cov_increment": 0.1
    }

    response = requests.post(
        f"{BASE_URL}/analog-inputs",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "Create Analog Input")
    return response.json().get('id') if response.status_code == 201 else None

def create_binary_input():
    """Create a binary input object."""
    data = {
        "object_identifier": 40001,
        "object_name": "Door_Sensor_1",
        "present_value": "active",
        "description": "Door open/close sensor",
        "status_flags": "0000",
        "event_state": "normal",
        "out_of_service": False,
        "polarity": "normal"
    }

    response = requests.post(
        f"{BASE_URL}/binary-inputs",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "Create Binary Input")
    return response.json().get('id') if response.status_code == 201 else None

def create_multi_state_input():
    """Create a multi-state input object."""
    data = {
        "object_identifier": 70001,
        "object_name": "HVAC_Mode_1",
        "present_value": 1,
        "description": "HVAC system mode",
        "status_flags": "0000",
        "event_state": "normal",
        "out_of_service": False,
        "number_of_states": 4,
        "state_text": ["Off", "Heat", "Cool", "Auto"]
    }

    response = requests.post(
        f"{BASE_URL}/multi-state-inputs",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "Create Multi-State Input")
    return response.json().get('id') if response.status_code == 201 else None

def list_objects(object_type):
    """List objects of a specific type."""
    response = requests.get(f"{BASE_URL}/{object_type}?page=1&page_size=10")
    print_response(response, f"List {object_type.replace('-', ' ').title()}")

def get_object(object_type, object_id):
    """Get a specific object by ID."""
    response = requests.get(f"{BASE_URL}/{object_type}/{object_id}")
    print_response(response, f"Get {object_type.replace('-', ' ').title()} {object_id}")

def update_object(object_type, object_id, update_data):
    """Update an object."""
    response = requests.put(
        f"{BASE_URL}/{object_type}/{object_id}",
        json=update_data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, f"Update {object_type.replace('-', ' ').title()} {object_id}")

def delete_object(object_type, object_id):
    """Delete an object."""
    response = requests.delete(f"{BASE_URL}/{object_type}/{object_id}")
    print_response(response, f"Delete {object_type.replace('-', ' ').title()} {object_id}")

def user_login():
    """User login."""
    data = {
        "name": "administrator",
        "password": "!BACnetPro1"
    }

    response = requests.post(
        f"{BASE_URL}/login",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "User Login")
    return response.json().get('user') if response.status_code == 200 else None

def user_logout(user_id=None, name=None):
    """User logout."""
    data = {}
    if user_id:
        data['user_id'] = user_id
    elif name:
        data['name'] = name

    response = requests.post(
        f"{BASE_URL}/logout",
        json=data,
        headers={'Content-Type': 'application/json'}
    )
    print_response(response, "User Logout")

def main():
    """Main function to run all examples."""
    print("XBACnet API Usage Examples")
    print("Make sure the API server is running on http://localhost:8000")

    # Test basic endpoints
    test_health_check()
    test_api_info()
    test_stats()

    # Test user authentication
    user = user_login()
    if user:
        user_logout(user_id=user['id'])

    # Create objects
    analog_id = create_analog_input()
    binary_id = create_binary_input()
    multi_state_id = create_multi_state_input()

    # List objects
    list_objects("analog-inputs")
    list_objects("binary-inputs")
    list_objects("multi-state-inputs")

    # Get specific objects
    if analog_id:
        get_object("analog-inputs", analog_id)
    if binary_id:
        get_object("binary-inputs", binary_id)
    if multi_state_id:
        get_object("multi-state-inputs", multi_state_id)

    # Update objects
    if analog_id:
        update_object("analog-inputs", analog_id, {"present_value": 26.0})
    if binary_id:
        update_object("binary-inputs", binary_id, {"present_value": "inactive"})
    if multi_state_id:
        update_object("multi-state-inputs", multi_state_id, {"present_value": 2})

    # Delete objects
    if analog_id:
        delete_object("analog-inputs", analog_id)
    if binary_id:
        delete_object("binary-inputs", binary_id)
    if multi_state_id:
        delete_object("multi-state-inputs", multi_state_id)

    print("\nExamples completed!")

if __name__ == "__main__":
    main()

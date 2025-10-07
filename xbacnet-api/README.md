# XBACnet API

REST API for managing BACnet objects in the XBACnet system.

## Prerequisites

- Python 3.10+ (required)
- MySQL 5.7+ or 8.0+
- pip (Python package manager)
- Docker 20.10+ (for containerized deployment)

## Features

- **RESTful API**: Full CRUD operations for all BACnet object types
- **Multiple Object Types**: Support for Analog, Binary, and Multi-state objects
- **Database Integration**: Direct integration with MySQL database
- **Data Validation**: JSON schema validation for all object properties
- **Pagination**: Built-in pagination support for large datasets
- **CORS Support**: Cross-origin resource sharing for web applications
- **Health Monitoring**: Health check and statistics endpoints
- **High Performance**: Built on Falcon framework with Gunicorn server

## Supported BACnet Object Types

- **Analog Objects**: Input, Output, Value
- **Binary Objects**: Input, Output, Value
- **Multi-state Objects**: Input, Output, Value

## API Endpoints

### Analog Objects
- `GET /api/analog-inputs` - List analog input objects
- `POST /api/analog-inputs` - Create analog input object
- `GET /api/analog-inputs/{id}` - Get analog input object by ID
- `PUT /api/analog-inputs/{id}` - Update analog input object
- `DELETE /api/analog-inputs/{id}` - Delete analog input object

Similar endpoints for analog-outputs and analog-values.

### Binary Objects
- `GET /api/binary-inputs` - List binary input objects
- `POST /api/binary-inputs` - Create binary input object
- `GET /api/binary-inputs/{id}` - Get binary input object by ID
- `PUT /api/binary-inputs/{id}` - Update binary input object
- `DELETE /api/binary-inputs/{id}` - Delete binary input object

Similar endpoints for binary-outputs and binary-values.

### Multi-state Objects
- `GET /api/multi-state-inputs` - List multi-state input objects
- `POST /api/multi-state-inputs` - Create multi-state input object
- `GET /api/multi-state-inputs/{id}` - Get multi-state input object by ID
- `PUT /api/multi-state-inputs/{id}` - Update multi-state input object
- `DELETE /api/multi-state-inputs/{id}` - Delete multi-state input object

Similar endpoints for multi-state-outputs and multi-state-values.

### User Management
- `GET /api/users` - List users
- `POST /api/users` - Create new user
- `GET /api/users/{id}` - Get user by ID
- `PUT /api/users/{id}` - Update user
- `DELETE /api/users/{id}` - Delete user
- `POST /api/login` - User authentication
- `POST /api/logout` - User logout

### Utility Endpoints
- `GET /api/health` - Health check endpoint
- `GET /api/stats` - Statistics about objects in database
- `GET /` - API information and documentation

## Installation

### Option 1: Docker Deployment

1. **Build Docker image**:
```bash
docker build -t xbacnet-api .
```

2. **Run Docker container**:
```bash
docker run -d -p 8000:8000 xbacnet-api
```

3. **Using build script**:
```bash
./docker-build.sh build-run
```

### Option 2: Local Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp env.example .env
# Edit .env with your database settings
```

3. **Start the server**:
```bash
python run.py
```

### Quick Docker Commands

```bash
# Build and run with custom script
./docker-build.sh build-run

# Manual Docker commands
docker build -t xbacnet-api .
docker run -d -p 8000:8000 xbacnet-api

# Stop container
./docker-build.sh stop
```

## Configuration

The API can be configured through environment variables or by editing the `.env` file:

- `XBACNET_DB_HOST`: Database host (default: localhost)
- `XBACNET_DB_PORT`: Database port (default: 3306)
- `XBACNET_DB_USER`: Database username (default: root)
- `XBACNET_DB_PASSWORD`: Database password
- `XBACNET_DB_NAME`: Database name (default: xbacnet)
- `XBACNET_API_HOST`: API host (default: 0.0.0.0)
- `XBACNET_API_PORT`: API port (default: 8000)
- `XBACNET_API_DEBUG`: Debug mode (default: False)

## Usage Examples

### Create an Analog Input Object
```bash
curl -X POST http://localhost:8000/api/analog-inputs \
  -H "Content-Type: application/json" \
  -d '{
    "object_identifier": 10001,
    "object_name": "Temperature_Sensor_1",
    "present_value": 25.5,
    "description": "Room temperature sensor",
    "status_flags": "0000",
    "event_state": "normal",
    "out_of_service": false,
    "units": "degreesCelsius",
    "cov_increment": 0.1
  }'
```

### Get All Analog Input Objects
```bash
curl http://localhost:8000/api/analog-inputs?page=1&page_size=10
```

### Update an Object
```bash
curl -X PUT http://localhost:8000/api/analog-inputs/1 \
  -H "Content-Type: application/json" \
  -d '{
    "present_value": 26.0,
    "description": "Updated temperature sensor"
  }'
```

### Delete an Object
```bash
curl -X DELETE http://localhost:8000/api/analog-inputs/1
```

### User Management Examples

#### Create a New User
```bash
curl -X POST http://localhost:8000/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe",
    "display_name": "John Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123",
    "is_admin": false
  }'
```

#### User Login
```bash
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe",
    "password": "securepassword123"
  }'
```

#### Get All Users
```bash
curl http://localhost:8000/api/users?page=1&page_size=10
```

#### Update User
```bash
curl -X PUT http://localhost:8000/api/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "John Smith",
    "email": "john.smith@example.com"
  }'
```

#### Delete User
```bash
curl -X DELETE http://localhost:8000/api/users/1
```

#### User Logout
```bash
curl -X POST http://localhost:8000/api/logout \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": 1
  }'
```

或者使用用户名：
```bash
curl -X POST http://localhost:8000/api/logout \
  -H "Content-Type: application/json" \
  -d '{
    "name": "john_doe"
  }'
```

## Development

### Running in Development Mode
```bash
python run.py --debug --reload
```

### Running Tests
```bash
pytest
```

## API Testing

### Postman
1. Download Postman from [https://www.postman.com/](https://www.postman.com/)
2. Import the `XBACnet_API_Postman.json` file into Postman
3. Configure the environment variable `baseUrl` to `http://localhost:8000`
4. Start testing all API endpoints

### Apipost
1. Download Apipost from [https://www.apipost.cn/](https://www.apipost.cn/)
2. Import the `XBACnet_API_Apipost.json` file into Apipost
3. Configure the environment variable `baseUrl` to `http://localhost:8000`
4. Start testing all API endpoints

### Quick Test Steps
1. Start the API server: `python run.py`
2. Run "Health Check" to verify server status
3. Test CRUD operations for different object types
4. Use the provided examples in the API collection

For detailed instructions, see:
- [Postman Import Guide](./Postman_Import_Guide.md)
- [Apipost Import Guide](./Apipost_Import_Guide.md)

## Architecture

The API is built using:
- **Falcon**: High-performance Python web framework
- **Gunicorn**: Python WSGI HTTP Server
- **MySQL Connector**: Direct MySQL database connectivity
- **JSON Schema**: Data validation
- **CORS**: Cross-origin support

## License

This project is part of the XBACnet system and follows the same license terms.

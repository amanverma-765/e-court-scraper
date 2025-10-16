"""
E-Courts API Documentation and Configuration Guide.

This module provides comprehensive documentation for the E-Courts REST API.

## Project Structure

The API follows a modular architecture:

```
api/
├── main.py                 # FastAPI application entry point
├── schemas.py              # Pydantic request/response models
├── exceptions.py           # Exception handlers
├── dependencies.py         # Dependency injection
└── routers/
    ├── __init__.py        # Authentication routes
    ├── cases.py           # Case-related routes
    └── cause_list.py      # Cause list and court routes

scraper/
├── auth_manager.py        # Authentication logic
├── case_manager.py        # Case-related business logic
└── cause_list_manager.py  # Cause list business logic

utils/
├── constants.py           # Configuration constants
├── exceptions.py          # Custom exceptions
├── crypto_utils.py        # Encryption/decryption utilities
└── cause_list_type.py     # Cause list type enum
```

## API Endpoints

### 1. Authentication

#### POST /auth/token
Generate JWT token for API authentication.

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated successfully",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

**Error Response:**
```json
{
  "status": "error",
  "code": 401,
  "message": "Authentication failed or token expired",
  "details": {
    "error": "Failed to authenticate with e-courts API"
  }
}
```

### 2. Case Endpoints

#### POST /cases/details
Retrieve case details by Case Number Reference (CNR).

**Request:**
```json
{
  "cnr": "UPBL060021142023"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Case details retrieved successfully",
  "data": {
    "case_number": "...",
    "case_status": "...",
    ...
  }
}
```

**Errors:**
- 400: Bad request (invalid CNR format)
- 401: Unauthorized (token invalid/expired)
- 404: Case not found
- 500: Internal server error

### 3. Court and Cause List Endpoints

#### GET /court/states
Retrieve all states available in e-courts system.

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "States retrieved successfully",
  "data": {
    "states": [
      {
        "state_code": "5",
        "state_name": "Uttar Pradesh"
      },
      ...
    ]
  }
}
```

#### POST /court/districts
Retrieve districts for a given state.

**Request:**
```json
{
  "state_code": "5"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Districts retrieved successfully",
  "data": {
    "districts": [
      {
        "district_code": "7",
        "district_name": "Lucknow"
      },
      ...
    ]
  }
}
```

#### POST /court/complex
Retrieve court complex for state and district.

**Request:**
```json
{
  "state_code": "5",
  "district_code": "7"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Court complex retrieved successfully",
  "data": {
    "court_complex": [...]
  }
}
```

#### POST /court/names
Retrieve court names for given parameters.

**Request:**
```json
{
  "state_code": "5",
  "district_code": "7",
  "court_code": "3"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Court names retrieved successfully",
  "data": {
    "courts": [...]
  }
}
```

#### POST /court/cause-list
Retrieve cause list for a specific court and date.

**Request:**
```json
{
  "state_code": "5",
  "district_code": "7",
  "court_code": "1",
  "court_number": "1",
  "cause_list_type": "CIVIL",
  "date": "16-10-2020"
}
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Cause list retrieved successfully",
  "data": {
    "cases": [...]
  }
}
```

**Parameters:**
- `cause_list_type`: Either "CIVIL" or "CRIMINAL"
- `date`: Format DD-MM-YYYY

#### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## Error Handling

All errors follow a consistent format:

```json
{
  "status": "error",
  "code": <HTTP_STATUS_CODE>,
  "message": "<Error description>",
  "details": {
    "error": "<Detailed error information>"
  }
}
```

### HTTP Status Codes:
- 200: OK
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 409: Conflict
- 422: Unprocessable Entity (Validation Error)
- 500: Internal Server Error

## Running the API

### Installation
```bash
pip install -r requirements.txt
```

### Start the Server
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI Schema: http://localhost:8000/openapi.json

## Authentication Flow

1. Call `/auth/token` to get JWT token
2. Use the token in subsequent requests via the `Authorization` header
3. Token is automatically injected via dependency injection

## Exception Handling Architecture

The API uses custom exception handlers for different error scenarios:

- `UnauthorizedException`: 401 Unauthorized
- `NotFoundException`: 404 Not Found
- `BadRequestException`: 400 Bad Request
- `ValidationException`: 422 Unprocessable Entity
- `ConflictException`: 409 Conflict
- `InternalServerErrorException`: 500 Internal Server Error

All custom exceptions are automatically converted to appropriate HTTP responses.

## Logging

Logging is configured at the module level with:
- Level: INFO
- Format: %(asctime)s - %(name)s - %(levelname)s - %(message)s

Logs include:
- API request/response information
- Error details with stack traces
- Authentication events
- Business logic execution

## Middleware

The API includes:
- **CORS Middleware**: Enables cross-origin requests
- **Trusted Host Middleware**: Restricts access to trusted hosts
- **Exception Handlers**: Global error handling

## Dependency Injection

FastAPI dependencies manage:
- HTTP client lifecycle
- Authentication token retrieval
- Request/response validation

## Configuration

Key configuration points:
- `HEADERS`: HTTP headers for API requests
- `BASE_URL`: E-courts API base URL
- `ENCRYPTION_KEY`: AES encryption key
- `DECRYPTION_KEY`: AES decryption key

All configuration is in `utils/constants.py` and `utils/crypto_utils.py`.
"""

# This is a documentation module - no runtime code

# E-Courts API

A comprehensive REST API interface for the Indian e-Courts system built with FastAPI. This API provides access to case information, court details, and cause lists with proper error handling and authentication.

## Features

✅ **JWT Authentication** - Secure token-based authentication
✅ **Case Management** - Retrieve case details by CNR (Case Number Reference)
✅ **Court Information** - Access states, districts, courts, and court complexes
✅ **Cause Lists** - Get cause lists for specific courts and dates
✅ **Error Handling** - Comprehensive error handling with detailed responses
✅ **Validation** - Input validation using Pydantic models
✅ **Logging** - Detailed logging for debugging and monitoring
✅ **API Documentation** - Auto-generated Swagger and ReDoc documentation

## Project Structure

```
e-court/
├── api/
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic request/response models
│   ├── exceptions.py        # Exception handlers
│   ├── dependencies.py      # Dependency injection
│   └── routers/
│       ├── __init__.py      # Authentication routes (/auth/token)
│       ├── cases.py         # Case routes (/cases/details)
│       └── cause_list.py    # Court routes (/court/*)
├── scraper/
│   ├── auth_manager.py      # Authentication logic
│   ├── case_manager.py      # Case business logic
│   └── cause_list_manager.py # Court/cause list business logic
├── utils/
│   ├── constants.py         # Configuration constants
│   ├── exceptions.py        # Custom exceptions
│   ├── crypto_utils.py      # Encryption/decryption
│   └── cause_list_type.py   # Type definitions
├── requirements.txt         # Python dependencies
└── main.py                 # Original CLI entry point
```

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository and navigate to the project directory:
```bash
cd e-court
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

### Development Server
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Production Server
```bash
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### 1. Health Check
```
GET /health
```
Check if the API is running.

### 2. Authentication
```
POST /auth/token
```
Generate JWT token for API authentication.

### 3. Case Details
```
GET /cases/details?cnr=UPBL060021142023
```
Retrieve case details by CNR (query parameter).

**Query Parameters:**
- `cnr` (required): Case Number Reference

### 4. Court Information

#### Get States
```
GET /court/states
```

#### Get Districts
```
POST /court/districts
{
  "state_code": "5"
}
```

#### Get Court Complex
```
POST /court/complex
{
  "state_code": "5",
  "district_code": "7"
}
```

#### Get Court Names
```
POST /court/names
{
  "state_code": "5",
  "district_code": "7",
  "court_code": "3"
}
```

#### Get Cause List
```
POST /court/cause-list
{
  "state_code": "5",
  "district_code": "7",
  "court_code": "1",
  "court_number": "1",
  "cause_list_type": "CIVIL",
  "date": "16-10-2020"
}
```

## API Documentation

### Interactive Swagger UI
Visit `http://localhost:8000/docs` in your browser to interact with the API

### ReDoc Documentation
Visit `http://localhost:8000/redoc` for alternative documentation

### OpenAPI Schema
Available at `http://localhost:8000/openapi.json`

## Error Handling

All errors follow a consistent response format:

```json
{
  "status": "error",
  "code": 400,
  "message": "Bad request",
  "details": {
    "error": "Detailed error information"
  }
}
```

### Common Error Codes
- **200**: Success
- **400**: Bad Request (validation error, invalid parameters)
- **401**: Unauthorized (authentication failed, invalid token)
- **404**: Not Found (resource doesn't exist)
- **409**: Conflict
- **422**: Unprocessable Entity (validation error)
- **500**: Internal Server Error

## Authentication Flow

1. **Get Token**: Call `/auth/token` endpoint
   ```bash
   curl http://localhost:8000/auth/token
   ```

2. **Use Token**: Include token in subsequent requests
   ```bash
   curl -H "Authorization: Bearer <token>" http://localhost:8000/court/states
   ```

3. **Automatic Injection**: Token is automatically injected via FastAPI dependencies

## Architecture

### Modular Design
- **Routers**: Separate routers for different resource types
- **Schemas**: Pydantic models for validation
- **Dependencies**: Centralized dependency injection
- **Exception Handlers**: Unified error handling

### Exception Handling
- Custom exceptions for different error scenarios
- Automatic conversion to HTTP responses
- Detailed error messages with context

### Logging
- Module-level logging configuration
- Request/response logging
- Error logging with stack traces
- Authentication event logging

## Configuration

### Update Requirements
```bash
pip install -r requirements.txt
```

### Environment Variables
Add these if needed:
- `LOG_LEVEL`: Logging level (default: INFO)
- `API_HOST`: API host (default: 0.0.0.0)
- `API_PORT`: API port (default: 8000)

## Example Usage

### Python Requests
```python
import requests

# Get token
token_response = requests.post('http://localhost:8000/auth/token')
token = token_response.json()['data']['token']

# Get case details
headers = {'Authorization': f'Bearer {token}'}
case_response = requests.get(
    'http://localhost:8000/cases/details',
    params={'cnr': 'UPBL060021142023'},
    headers=headers
)
print(case_response.json())
```

### cURL
```bash
# Get token
curl -X POST http://localhost:8000/auth/token

# Get case details (replace TOKEN with actual token)
curl -X GET http://localhost:8000/cases/details?cnr=UPBL060021142023 \
  -H "Authorization: Bearer TOKEN"
```

## Development

### Adding New Endpoints

1. Create schemas in `api/schemas.py`
2. Create route handler in `api/routers/`
3. Implement business logic in `scraper/`
4. Include router in `api/main.py`

### Example Router
```python
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/new", tags=["New"])

@router.get("/endpoint")
async def new_endpoint(token: str = Depends(get_auth_token)):
    # Implementation
    pass
```

## Testing

To test the API locally:

```bash
# Start the server
python -m uvicorn api.main:app --reload

# In another terminal, test endpoints
curl http://localhost:8000/health
curl http://localhost:8000/auth/token
```

## Troubleshooting

### Token Generation Fails
- Ensure network connectivity to e-courts API
- Check if authentication credentials are valid

### "No data found" errors
- Verify parameters (state_code, district_code, etc.)
- Check date format (DD-MM-YYYY)

### Connection Timeouts
- Increase timeout in `api/dependencies.py`
- Check network connectivity
- Verify firewall rules

## Performance Considerations

- HTTP client connection pooling is enabled
- Timeout is set to 20 seconds (configurable)
- Logging can be adjusted based on requirements

## Security

- CORS middleware is configured
- Trusted host validation is enabled
- Authentication is required for most endpoints
- Input validation using Pydantic models

## Dependencies

See `requirements.txt` for all dependencies:
- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `httpx`: HTTP client
- `pydantic`: Data validation
- `pycryptodome`: Cryptography

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues or questions, please contact the development team.

---

**API Version**: 1.0.0
**Last Updated**: October 2025

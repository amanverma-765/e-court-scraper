# E-Courts API

REST API for accessing Indian e-Courts data with JWT authentication.

## Features

- 🔐 JWT-based authentication
- 🏛️ Access to Indian e-Courts data
- 📋 Cause lists, case details, court information
- 🔒 Per-request HTTP client isolation
- 📚 Interactive API documentation (Swagger UI)
- 🔄 Automatic token encryption for e-courts backend

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/amanverma-765/e-court-scraper.git
cd e-court-scraper

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run the API

```bash
python run_api.py
```

Or:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

## Usage

### 1. Generate JWT Token

```bash
curl -X POST http://localhost:8000/auth/token
```

Response:
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated. Use in Authorization header",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJ..."
  }
}
```

### 2. Use Token in Requests

```bash
TOKEN="your_token_here"

# Get all states
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer $TOKEN"

# Get districts by state
curl -X POST "http://localhost:8000/court/districts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state_code": "1"}'

# Get case details
curl -X GET "http://localhost:8000/cases/details?cnr=DLHC010123452024" \
  -H "Authorization: Bearer $TOKEN"
```

## API Documentation

### Interactive Docs

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

**Using Swagger UI:**
1. Generate token from `/auth/token` endpoint
2. Click the 🔓 **Authorize** button (top right)
3. Paste your token (without "Bearer" prefix)
4. Click **Authorize**
5. All endpoints now work automatically!

### Endpoints

#### Authentication
- `POST /auth/token` - Generate JWT token (no auth required)

#### Court & Cause List
- `GET /court/states` - Get all states
- `POST /court/districts` - Get districts by state code
- `POST /court/complex` - Get court complex information
- `POST /court/names` - Get court names
- `POST /court/cause-list` - Get cause list for a court

#### Cases
- `GET /cases/details?cnr=<CNR>` - Get case details by CNR

#### Health
- `GET /health` - Health check endpoint
- `GET /` - API information

For detailed API documentation, see [API_DOCS.md](API_DOCS.md)

## Project Structure

```
e-court/
├── api/
│   ├── dependencies.py      # FastAPI dependencies (auth, HTTP client)
│   ├── exceptions.py         # Exception handlers
│   ├── main.py              # FastAPI application
│   ├── schemas.py           # Pydantic models
│   └── routers/
│       ├── auth.py          # Authentication endpoints
│       ├── cases.py         # Case-related endpoints
│       └── cause_list.py    # Court & cause list endpoints
├── scraper/
│   ├── auth_manager.py      # JWT token generation
│   ├── case_manager.py      # Case data scraping
│   └── cause_list_manager.py # Court data scraping
├── utils/
│   ├── constants.py         # Configuration constants
│   ├── crypto_utils.py      # Encryption/decryption utilities
│   ├── exceptions.py        # Custom exceptions
│   └── cause_list_type.py   # Enums for cause list types
├── requirements.txt         # Python dependencies
├── run_api.py              # API runner script
└── README.md               # This file
```

## Requirements

- Python 3.10+
- httpx
- fastapi
- uvicorn
- pycryptodome
- pydantic

See `requirements.txt` for complete list.

## Architecture

### JWT Authentication Flow

```
1. Client → POST /auth/token
   ↓
2. API generates token from e-courts backend
   ↓
3. Client stores token
   ↓
4. Client → Any endpoint with "Authorization: Bearer <token>"
   ↓
5. API validates token
   ↓
6. API creates isolated HTTP client
   ↓
7. API encrypts token for e-courts backend
   ↓
8. API fetches data from e-courts
   ↓
9. API returns data to client
   ↓
10. HTTP client closed (per-request isolation)
```

### Security Features

- **Per-request HTTP clients**: Each API call gets its own isolated HTTP client
- **JWT validation**: Tokens are validated on every request
- **Token encryption**: Tokens are encrypted before sending to e-courts backend
- **User context isolation**: No data leakage between users

## Configuration

Key configuration in `utils/constants.py`:
- `BASE_URL`: E-courts API base URL
- `DEVICE_ID`: Device identifier for authentication

Encryption keys in `utils/crypto_utils.py`:
- `ENCRYPTION_KEY`: For request encryption
- `DECRYPTION_KEY`: For response decryption

## Development

### Running Tests

```bash
python test_jwt_workflow.py
```

### Code Style

The codebase follows clean code principles:
- No unnecessary comments
- Concise function names
- Essential logging only
- Type hints where beneficial

## Error Handling

Common errors:

**401 Unauthorized**
- Missing or invalid JWT token
- Solution: Generate a new token from `/auth/token`

**404 Not Found**
- Data not available in e-courts system
- Invalid CNR, state code, etc.

**500 Internal Server Error**
- E-courts backend issues
- Network problems

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and research purposes.

## Disclaimer

This API is not officially affiliated with e-Courts India. Use responsibly and in accordance with e-Courts terms of service.

## Support

For issues and questions:
- Create an issue on GitHub
- Check existing documentation in `API_DOCS.md`

---

**Note**: E-courts tokens expire quickly (~10 minutes). Generate fresh tokens when you encounter authorization errors.

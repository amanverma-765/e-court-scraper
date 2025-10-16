# E-Courts API - Quick Reference Guide

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the API
python -m uvicorn api.main:app --reload

# 3. Open browser to http://localhost:8000/docs
```

## 📋 API Endpoints

### Authentication
```
POST /auth/token
```
Get JWT token for API access.

### Case Management
```
GET /cases/details?cnr=UPBL060021142023
```
Get case details by CNR (query parameter).

### Court Information

Get all states:
```
GET /court/states
```

Get districts by state:
```
POST /court/districts
{
  "state_code": "5"
}
```

Get court complex:
```
POST /court/complex
{
  "state_code": "5",
  "district_code": "7"
}
```

Get court names:
```
POST /court/names
{
  "state_code": "5",
  "district_code": "7",
  "court_code": "3"
}
```

Get cause list:
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

## 🏗️ Project Structure

```
api/
├── main.py              # FastAPI app
├── schemas.py           # Pydantic models
├── exceptions.py        # Error handlers
├── dependencies.py      # Dependencies
└── routers/
    ├── __init__.py      # Auth routes
    ├── cases.py         # Case routes
    └── cause_list.py    # Court routes
```

## 📚 Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI**: http://localhost:8000/openapi.json

## 🔍 Response Format

Success:
```json
{
  "status": "success",
  "code": 200,
  "message": "...",
  "data": {}
}
```

Error:
```json
{
  "status": "error",
  "code": 400,
  "message": "...",
  "details": {}
}
```

## 🛡️ Error Codes

- 200: Success
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 422: Validation Error
- 500: Server Error

## 💻 Example Usage

### Python
```python
import httpx

async with httpx.AsyncClient() as client:
    # Get token
    resp = await client.post('http://localhost:8000/auth/token')
    token = resp.json()['data']['token']
    
    # Get case details
    resp = await client.post(
        'http://localhost:8000/cases/details',
        json={'cnr': 'UPBL060021142023'},
        headers={'Authorization': f'Bearer {token}'}
    )
    print(resp.json())
```

### cURL
```bash
# Get token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/token | jq -r '.data.token')

# Get case details
curl -X POST http://localhost:8000/cases/details \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"cnr": "UPBL060021142023"}'
```

## 📝 Available Cause List Types

- `CIVIL`: Civil cases
- `CRIMINAL`: Criminal cases

## 🔐 Authentication

All endpoints except `/auth/token` require a JWT token:

```
Authorization: Bearer <token>
```

Token is automatically managed by FastAPI dependencies.

## 📁 File Organization

| File | Purpose | Lines |
|------|---------|-------|
| api/main.py | FastAPI app, routers, middleware | 130 |
| api/schemas.py | Pydantic models | 200+ |
| api/exceptions.py | Exception handlers | 130+ |
| api/dependencies.py | Dependency injection | 65 |
| api/routers/__init__.py | Auth endpoint | 60 |
| api/routers/cases.py | Case endpoint | 80 |
| api/routers/cause_list.py | Court endpoints | 250+ |

## 🧪 Testing Endpoints

Health check:
```bash
curl http://localhost:8000/health
```

Get token:
```bash
curl -X POST http://localhost:8000/auth/token
```

## ⚙️ Configuration

Edit these files to configure:

- `api/main.py`: App settings, CORS, middleware
- `api/dependencies.py`: HTTP client settings
- `utils/constants.py`: API constants
- `requirements.txt`: Dependencies

## 🐛 Debugging

Check logs:
```bash
# Enable debug logging by modifying api/main.py
logging.basicConfig(level=logging.DEBUG)
```

## 📦 Dependencies

- `fastapi`: Web framework
- `uvicorn`: ASGI server
- `httpx`: HTTP client
- `pydantic`: Data validation
- `pycryptodome`: Cryptography

## 🚫 Troubleshooting

### Port already in use
```bash
python -m uvicorn api.main:app --port 8001
```

### ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Authentication fails
- Check internet connectivity
- Verify e-courts API is accessible
- Check network logs

## 📞 API Support

- Check `/docs` for interactive documentation
- Review error messages in response
- Check server logs for details
- See API_README.md for detailed docs

## 🎯 Common Tasks

### Add new endpoint
1. Create schema in `api/schemas.py`
2. Create route in `api/routers/new_file.py`
3. Include router in `api/main.py`

### Modify error handling
Edit `api/exceptions.py`

### Change HTTP client settings
Edit `api/dependencies.py`

### Add CORS origin
Edit `api/main.py` CORS middleware

## ✅ Checklist Before Production

- [ ] Disable reload mode in uvicorn
- [ ] Use HTTPS
- [ ] Configure CORS for specific origins
- [ ] Set up rate limiting
- [ ] Configure logging for production
- [ ] Set token expiration
- [ ] Enable request/response compression
- [ ] Add monitoring and alerting

---

**Version**: 1.0.0 | **Last Updated**: October 2025

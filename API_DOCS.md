# API Documentation

Complete API reference for E-Courts API.

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except `/auth/token` and `/health`) require JWT authentication.

### Header Format

```
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

**Endpoint:** `POST /auth/token`

**Request:**
```bash
curl -X POST http://localhost:8000/auth/token
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated. Use in Authorization header",
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Note:** Tokens expire in ~10 minutes. Generate a new token when you receive 401 errors.

---

## Endpoints

### Authentication

#### POST /auth/token

Generate a JWT token for API authentication.

**Authentication Required:** No

**Request:**
- No parameters required

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated. Use in Authorization header",
  "data": {
    "token": "string"
  }
}
```

**Status Codes:**
- `200` - Token generated successfully
- `500` - Failed to generate token

---

### Court & Cause List

#### GET /court/states

Get list of all states in e-courts system.

**Authentication Required:** Yes

**Request:**
```bash
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "States retrieved",
  "data": {
    "state_list": [
      {
        "state_code": "1",
        "state_name": "Andhra Pradesh"
      },
      {
        "state_code": "2",
        "state_name": "Arunachal Pradesh"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - States retrieved successfully
- `401` - Unauthorized (missing/invalid token)
- `404` - Data not found
- `500` - Internal server error

---

#### POST /court/districts

Get districts for a specific state.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "state_code": "string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/court/districts" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"state_code": "1"}'
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Districts retrieved",
  "data": {
    "district_list": [
      {
        "district_code": "1",
        "district_name": "Anantapur"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - Districts retrieved successfully
- `400` - Bad request (invalid state code)
- `401` - Unauthorized
- `404` - Districts not found
- `500` - Internal server error

---

#### POST /court/complex

Get court complex information for a state and district.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "state_code": "string",
  "district_code": "string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/court/complex" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "state_code": "1",
    "district_code": "1"
  }'
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Court complex retrieved",
  "data": {
    "court_complex_list": [
      {
        "court_code": "1",
        "court_complex_name": "District Court Complex"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - Court complex retrieved successfully
- `400` - Bad request
- `401` - Unauthorized
- `404` - Data not found
- `500` - Internal server error

---

#### POST /court/names

Get court names for a specific state, district, and court code.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "state_code": "string",
  "district_code": "string",
  "court_code": "string"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/court/names" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "state_code": "1",
    "district_code": "1",
    "court_code": "1"
  }'
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Court names retrieved",
  "data": {
    "court_list": [
      {
        "court_number": "1",
        "court_name": "Court No. 1"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - Court names retrieved successfully
- `400` - Bad request
- `401` - Unauthorized
- `404` - Data not found
- `500` - Internal server error

---

#### POST /court/cause-list

Get cause list for a specific court, date, and type.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "state_code": "string",
  "district_code": "string",
  "court_code": "string",
  "court_number": "string",
  "cause_list_type": "CIVIL" | "CRIMINAL",
  "date": "DD-MM-YYYY"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/court/cause-list" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "state_code": "1",
    "district_code": "1",
    "court_code": "1",
    "court_number": "1",
    "cause_list_type": "CIVIL",
    "date": "16-10-2025"
  }'
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Cause list retrieved",
  "data": {
    "cases": [
      {
        "case_number": "CS/123/2024",
        "filing_date": "01-01-2024",
        "party_names": "ABC vs XYZ",
        "stage": "Hearing"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - Cause list retrieved successfully
- `400` - Bad request (invalid cause list type, must be 'CIVIL' or 'CRIMINAL')
- `401` - Unauthorized
- `404` - Data not found
- `500` - Internal server error

---

### Cases

#### GET /cases/details

Get detailed information about a case using its CNR (Case Number Reference).

**Authentication Required:** Yes

**Query Parameters:**
- `cnr` (required): Case Number Reference

**Example:**
```bash
curl -X GET "http://localhost:8000/cases/details?cnr=DLHC010123452024" \
  -H "Authorization: Bearer <token>"
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Case details retrieved",
  "data": {
    "case_number": "CS/123/2024",
    "filing_date": "01-01-2024",
    "registration_date": "02-01-2024",
    "case_type": "Civil Suit",
    "petitioner": "ABC Company Ltd.",
    "respondent": "XYZ Corporation",
    "petitioner_advocate": "Adv. John Doe",
    "respondent_advocate": "Adv. Jane Smith",
    "case_status": "Pending",
    "next_hearing_date": "20-10-2025",
    "history": [
      {
        "date": "15-10-2025",
        "proceeding": "Case listed for hearing"
      }
    ]
  }
}
```

**Status Codes:**
- `200` - Case details retrieved successfully
- `400` - Bad request (invalid CNR format)
- `401` - Unauthorized
- `404` - Case not found
- `500` - Internal server error

---

### Health

#### GET /health

Check API health status.

**Authentication Required:** No

**Request:**
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

**Status Codes:**
- `200` - API is healthy

---

#### GET /

Get API information.

**Authentication Required:** No

**Request:**
```bash
curl -X GET "http://localhost:8000/"
```

**Response:**
```json
{
  "message": "Welcome to E-Courts API",
  "version": "1.0.0",
  "docs": "/docs"
}
```

**Status Codes:**
- `200` - Success

---

## Error Responses

All error responses follow this format:

```json
{
  "status": "error",
  "code": 401,
  "message": "Authorization required. Use 🔓 Authorize button or add 'Authorization: Bearer <token>' header"
}
```

### Common Error Codes

- `400 Bad Request` - Invalid input parameters
- `401 Unauthorized` - Missing or invalid authentication token
- `404 Not Found` - Requested resource not found
- `500 Internal Server Error` - Server-side error or e-courts backend issue

---

## Rate Limiting

Currently, there is no rate limiting. Use responsibly.

---

## Using with Swagger UI

1. Open http://localhost:8000/docs
2. Generate token from `POST /auth/token`
3. Copy the token value
4. Click 🔓 **Authorize** button (top right)
5. Paste token (without "Bearer" prefix)
6. Click **Authorize** and **Close**
7. All endpoints now include your token automatically!

---

## Code Examples

### Python (httpx)

```python
import httpx

BASE_URL = "http://localhost:8000"

# Generate token
client = httpx.Client()
response = client.post(f"{BASE_URL}/auth/token")
token = response.json()["data"]["token"]

# Use token in requests
headers = {"Authorization": f"Bearer {token}"}

# Get states
response = client.get(f"{BASE_URL}/court/states", headers=headers)
states = response.json()

# Get case details
response = client.get(
    f"{BASE_URL}/cases/details",
    params={"cnr": "DLHC010123452024"},
    headers=headers
)
case_details = response.json()

client.close()
```

### JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";

// Generate token
const tokenResponse = await fetch(`${BASE_URL}/auth/token`, {
  method: "POST"
});
const tokenData = await tokenResponse.json();
const token = tokenData.data.token;

// Use token in requests
const headers = {
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
};

// Get states
const statesResponse = await fetch(`${BASE_URL}/court/states`, { headers });
const states = await statesResponse.json();

// Get districts
const districtsResponse = await fetch(`${BASE_URL}/court/districts`, {
  method: "POST",
  headers,
  body: JSON.stringify({ state_code: "1" })
});
const districts = await districtsResponse.json();
```

### cURL

```bash
# Generate token and store in variable
TOKEN=$(curl -s -X POST http://localhost:8000/auth/token | jq -r '.data.token')

# Use token in subsequent requests
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer $TOKEN"

curl -X POST "http://localhost:8000/court/districts" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"state_code": "1"}'
```

---

## Best Practices

1. **Token Management**
   - Store tokens securely
   - Regenerate tokens when they expire
   - Don't hardcode tokens in source code

2. **Error Handling**
   - Always check response status codes
   - Implement retry logic for 401 errors (regenerate token)
   - Handle 404 errors gracefully

3. **Performance**
   - Reuse tokens for multiple requests
   - Don't generate new token for every request
   - Close HTTP connections properly

4. **Security**
   - Use HTTPS in production
   - Don't log or expose tokens
   - Validate all user inputs

---

## Troubleshooting

### "Authorization header is required"
**Solution:** Make sure you're including the Authorization header in your request:
```
Authorization: Bearer <your_token>
```

### "Token cannot be empty"
**Solution:** Ensure the token is not empty and is properly formatted.

### "UnAuthorized" from e-courts backend
**Solution:** Token has expired. Generate a new token from `/auth/token`.

### 404 errors for valid data
**Solution:** Data might not be available in e-courts system. Verify the codes/CNR you're using.

---

## API Limits

- Token expiry: ~10 minutes
- No explicit rate limits (use responsibly)
- Large datasets may take time to fetch

---

## Support

For issues or questions:
- Check this documentation
- Review the README.md
- Open an issue on GitHub
- Check API logs for detailed error messages

---

**Last Updated:** October 16, 2025

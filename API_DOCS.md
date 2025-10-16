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

**Token Details:**
- Tokens are generated from the e-courts backend
- Token expiry: ~10 minutes (600 seconds)
- When token expires, you'll receive a 401 error with message: "Token expired or invalid"
- Generate a new token from `/auth/token` and use it in subsequent requests

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
    "states": [
      {
        "state_code": 1,
        "state_name": "Maharashtra",
        "marstate_name": "महाराष्ट्र",
        "nationalstate_code": "MH",
        "st_census_code": 27,
        "state_lang": "marathi",
        "bilingual": "Y",
        "state_name_marathi": "महाराष्ट्र",
        "state_name_hindi": "महाराष्ट्र",
        "state_name_gujrati": "મહારાષ્ટ્ર",
        "state_name_kannada": "ಮಹಾರಾಷ್ಟ್ರ",
        "state_name_tamil": "மகாராஷ்டிரா",
        "esummons_sharing": "Y"
      },
      {
        "state_code": 2,
        "state_name": "Andhra Pradesh",
        "marstate_name": "",
        "nationalstate_code": "AP",
        "st_census_code": 28,
        "state_lang": "",
        "bilingual": "N",
        "state_name_marathi": "आंध्र प्रदेश ",
        "state_name_hindi": "आंध्र प्रदेश",
        "state_name_gujrati": "આન્ધ્ર પ્રદેશ",
        "state_name_kannada": "ಆಂಧ್ರಪ್ರದೇಶ",
        "state_name_tamil": "ஆந்திரப் பிரதேசம்",
        "esummons_sharing": "Y"
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
    "districts": [
      {
        "dist_code": 26,
        "dist_name": "Ahmednagar",
        "mardist_name": "अहमदनगर",
        "dist_census_code": 522,
        "lg_dist_code": 466
      },
      {
        "dist_code": 5,
        "dist_name": "Akola",
        "mardist_name": "अकोला",
        "dist_census_code": 501,
        "lg_dist_code": 467
      },
      {
        "dist_code": 7,
        "dist_name": "Amravati",
        "mardist_name": "अमरावती",
        "dist_census_code": 503,
        "lg_dist_code": 468
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
    "courtComplex": [
      {
        "complex_code": 1010306,
        "njdg_est_code": "14",
        "court_complex_name": "Rahuri, Civil and Criminal Court",
        "lcourt_complex_name": "दिवाणी न्यायाधीश, कनिष्ठ स्तर आणि प्रथमवर्ग न्यायदंडाधिकारी, यांचे न्यायालय, राहुरी ४१३७०५",
        "njdg_state_code": 1,
        "njdg_dist_code": 26,
        "differ_mast_est": "N",
        "14": {
          "14": {
            "db_name": "ahmrahuricjjd",
            "court_name": "Civil Court Junior Division, Rahuri",
            "mcourt_name": "दिवाणी न्यायालय कनिष्ट स्तर, राहूरी",
            "server_ip": "10.192.102.226",
            "court_code": 14,
            "national_court_code": "MHAH18"
          }
        }
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
    "courtNames": "0~Select Court Name#D~--------Civil Court Junior Division, Rahuri--------#14^2~2-Shri. Pankaj H. Patil-2nd Jt. Civil Judge J.D. And JMFC#14^10~10-Smt. Anupama C. Parshetti-Jt Civil Judge J.D. And JMFC#14^11~11-Shri. A. K. Shinde-3rd Jt Civil Judge JD and JMFC#14^12~12-Shri. M. E. Pawar-Civil Judge Senior Division"
  }
}
```

**Note:** The response is a specially formatted string where:
- `#` separates entries
- `^` separates court code and details
- `~` separates different fields within an entry

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
    "cases": "<div id='table_heading'><center><center>Shri. Pankaj H. Patil<br/>2nd Jt. Civil Judge J.D. And JMFC</center>Civil Cases Listed on 16-10-2025</center></div><table width='80%' align='center' class='table table-responsive table-bordered' cellspacing='0' cellpadding='0' border='1'><thead style='text-align:center;'><th style='text-align:center'>Sr No</th><th style='text-align:center'>Case Number</th><th style='text-align:center'>Party Name</th><th style='text-align:center'>Advocate</th></thead><tbody><tr><td colspan='4' style='color:#3880d4'>Urgent Cases</td></tr><tr><td>1</td><td>R.C.S./633/2019<br/>16-10-2025</td><td>Jalindar Soma Dhanvade<br/>versus<br/>Sharda Babasaheb Bhambal</td><td>Kobarne V. G.<br/><br/>Dolse T. B.</td></tr></tbody></table>"
  }
}
```

**Note:** The response contains an HTML table with the cause list. You may need to parse the HTML to extract structured data.

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
    "history": {
      "regcase_type": 1,
      "date_of_filing": "2024-01-08",
      "cino": "MHAH010002332024",
      "dt_regis": "2024-01-15",
      "fil_no": 170,
      "fil_year": 2024,
      "reg_no": 10,
      "reg_year": 2024,
      "date_first_list": "2024-01-18",
      "date_next_list": "2025-11-21",
      "case_no": "200100000102024",
      "type_name": "R.C.A.",
      "ltype_name": "नियमित दिवाणी अपील",
      "pet_name": "Vilas Vitthal Kadus",
      "lpet_name": "विलास विठ्ठल कडुस",
      "pet_adv": "Athare P. V.",
      "lpet_adv": "आठरे पी. व्ही.",
      "res_name": "Chandar Mahammad Pawar",
      "lres_name": "चंदर महंमद पवार",
      "res_adv": "NIL",
      "lres_adv": "माहीती अपूर्ण",
      "case_status": "Pending",
      "purpose_name": "Awaiting Notice",
      "lpurpose_name": "नोटीस येणेसाठी",
      "court_no": 11,
      "date_last_list": "2025-10-10"
    }
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

### 401 Unauthorized - Missing Token

**Request without Authorization header:**
```bash
curl -X GET "http://localhost:8000/court/states"
```

**Response:**
```json
{
  "detail": "Authorization required. Use 'Authorization: Bearer <token>' header"
}
```

### 401 Unauthorized - Invalid/Expired Token

**Request with invalid token:**
```bash
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer invalid_token"
```

**Response:**
```json
{
  "status": "error",
  "code": 401,
  "message": "Authentication failed or token expired",
  "details": {
    "error": "Token expired or invalid. Generate a new token from /auth/token"
  }
}
```

### Common Error Codes

- `400 Bad Request` - Invalid input parameters (e.g., invalid cause_list_type, missing required fields)
- `401 Unauthorized` - Missing, invalid, or expired authentication token
- `404 Not Found` - Requested resource not found (no data available for given parameters)
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

## Data Format Notes

### Response Structures

Different endpoints return data in different formats based on how the e-courts backend provides them:

1. **States & Districts**: Returns structured JSON arrays with objects
2. **Court Complex**: Returns nested JSON with complex structure including database connection details
3. **Court Names**: Returns a **specially formatted string** (not array) with delimiters:
   - `#` separates entries
   - `^` separates court code and details  
   - `~` separates fields within an entry
   - You'll need to parse this string to extract court information

4. **Cause List**: Returns an **HTML table** as a string
   - Contains formatted HTML with court listings
   - You may need to parse HTML to extract structured data
   - Includes case numbers, party names, advocates, and hearing dates

5. **Case Details**: Returns structured JSON with comprehensive case information
   - Includes bilingual fields (English and regional language)
   - Contains filing dates, party names, advocates, case status, and hearing dates

### Multilingual Support

Many fields include both English and regional language versions:
- `state_name` and `marstate_name` (Marathi)
- `pet_name` (petitioner) and `lpet_name` (local language)
- `type_name` (case type) and `ltype_name` (local language)

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

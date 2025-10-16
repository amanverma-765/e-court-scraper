# JWT Authentication Workflow

## Overview
The API now requires users to generate and manage their own JWT tokens for authentication. Each request must include a valid JWT token in the Authorization header.

## Architecture Changes

### 1. **Per-Request HTTP Clients**
- Each API request creates its own isolated HTTP client
- Ensures user context separation and prevents cross-user data leakage
- Clients are automatically closed after request completion

### 2. **User-Provided JWT Tokens**
- Users must obtain a JWT token via the `/auth/token` endpoint
- This token must be passed in the Authorization header for all subsequent requests
- Tokens are validated on each request

## How to Use

### Step 1: Generate JWT Token

**Request:**
```bash
curl -X POST "http://localhost:8000/auth/token"
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated successfully. Use this token in Authorization header as 'Bearer <token>' for all API requests",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Step 2: Use Token in Subsequent Requests

**Example - Fetch States:**
```bash
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example - Get Case Details:**
```bash
curl -X GET "http://localhost:8000/cases/details?cnr=DLHC010123452024" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

**Example - Fetch Districts:**
```bash
curl -X POST "http://localhost:8000/court/districts" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -H "Content-Type: application/json" \
  -d '{"state_code": "1"}'
```

## Token Flow Diagram

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       │ 1. POST /auth/token
       ▼
┌─────────────────────────────────────┐
│  E-Courts API                       │
│  ┌──────────────────────────────┐  │
│  │  Generate JWT via e-courts   │  │
│  │  backend (get_jwt_token)     │  │
│  └──────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │ 2. Returns JWT token
       ▼
┌─────────────┐
│   Client    │ Stores token
└──────┬──────┘
       │
       │ 3. GET/POST /court/* or /cases/*
       │    with "Authorization: Bearer <token>"
       ▼
┌─────────────────────────────────────┐
│  E-Courts API                       │
│  ┌──────────────────────────────┐  │
│  │  Extract token from header   │  │
│  │  (get_auth_token dependency) │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Create per-request client   │  │
│  │  (get_http_client)           │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Encrypt token & call        │  │
│  │  e-courts backend API        │  │
│  │  (scraper functions)         │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Close HTTP client           │  │
│  └──────────────────────────────┘  │
└──────┬──────────────────────────────┘
       │ 4. Returns data
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

## Token Encryption Details

### Internal Process
1. **User receives plain JWT token** from `/auth/token` endpoint
2. **User passes plain JWT** in Authorization header to other endpoints
3. **API extracts plain JWT** from header
4. **API encrypts the JWT** using AES encryption before sending to e-courts backend
5. E-courts backend validates the encrypted token

### Why This Design?
- **Simplicity**: Users work with plain JWT tokens (standard practice)
- **Security**: Encryption happens server-side, protecting the e-courts API communication
- **Compatibility**: Follows standard Authorization header patterns

## Error Handling

### Missing Authorization Header
**Response:**
```json
{
  "status": "error",
  "code": 401,
  "message": "Authorization header is required. Please provide JWT token using 'Authorization: Bearer <token>' header"
}
```

### Invalid Authorization Format
**Response:**
```json
{
  "status": "error",
  "code": 401,
  "message": "Invalid authorization header format. Use 'Authorization: Bearer <token>'"
}
```

### Unauthorized (Invalid/Expired Token)
**Response:**
```json
{
  "status": "error",
  "code": 401,
  "message": "Request unauthorised: [error details]"
}
```

## Best Practices

1. **Store Token Securely**: Keep the JWT token secure in your application
2. **Handle Expiration**: Be prepared to regenerate tokens if they expire (401 responses)
3. **Per-Request Token**: Always include the token in each request
4. **Don't Share Tokens**: Each user/session should have its own token

## Technical Implementation

### Dependencies (`api/dependencies.py`)
- `get_http_client()`: Creates a new HTTP client per request
- `get_auth_token()`: Extracts and validates JWT from Authorization header

### Token Flow
1. Client calls `/auth/token` → receives JWT
2. Client includes JWT in `Authorization: Bearer <token>` header
3. `get_auth_token()` dependency extracts token
4. `get_http_client()` creates isolated HTTP client
5. Scraper functions receive plain token, encrypt it, and call e-courts backend
6. HTTP client is closed after response

## Migration Notes

### Previous Behavior
- API automatically generated tokens for each request
- Single global HTTP client shared across all users
- No user-provided authentication

### New Behavior
- Users generate and manage their own tokens
- Per-request HTTP clients for isolation
- Standard Authorization header pattern
- Better security and user context separation

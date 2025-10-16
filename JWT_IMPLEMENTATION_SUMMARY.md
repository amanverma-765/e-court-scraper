# JWT Management Implementation Summary

## Overview
Successfully implemented user-managed JWT authentication with per-request HTTP client isolation.

## Changes Made

### 1. **api/dependencies.py**
#### Before:
- Global HTTP client shared across all users
- `get_auth_token()` automatically generated JWT for each request
- No token extraction from headers

#### After:
- `get_http_client()` creates **per-request** HTTP clients for user isolation
- `get_auth_token()` extracts JWT from `Authorization: Bearer <token>` header
- Validates token format and presence
- Returns plain JWT token (not encrypted)

**Key Code:**
```python
async def get_auth_token(authorization: Optional[str] = Header(None)) -> str:
    """Extract and validate JWT token from Authorization header."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is required...")
    
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format...")
    
    return parts[1]  # Return plain JWT token
```

### 2. **api/main.py**
#### Changes:
- Removed global HTTP client lifecycle management
- Removed `get_http_client()` and `close_http_client()` imports from startup/shutdown
- Simplified lifespan context manager

### 3. **api/routers/auth.py**
#### Changes:
- Updated `/auth/token` endpoint description to explain token usage
- Added `finally` block to close HTTP client after token generation
- Enhanced response message to guide users

**Usage:**
```bash
POST /auth/token
# Response includes token to use in subsequent requests
```

### 4. **api/routers/cases.py**
#### Changes:
- Added `finally` block to close HTTP client after request
- Token now comes from user-provided Authorization header (via dependency)

### 5. **api/routers/cause_list.py**
#### Changes:
- Added `finally` blocks to all 5 endpoints:
  - `/court/states`
  - `/court/districts`
  - `/court/complex`
  - `/court/names`
  - `/court/cause-list`
- Each endpoint closes HTTP client after use

## Token Flow Architecture

### Previous Flow (❌ Problematic):
```
User Request → API generates token → Uses token → Returns data
                ↓
         Global HTTP Client (shared across all users)
```

### New Flow (✅ Secure):
```
1. User: POST /auth/token
   ← API generates JWT using e-courts backend
   
2. User stores JWT token

3. User: GET/POST /endpoint with "Authorization: Bearer <token>"
   → API extracts token from header
   → Creates isolated HTTP client
   → Encrypts token for e-courts backend
   → Calls e-courts API
   → Closes HTTP client
   ← Returns data
```

## Security Improvements

### 1. **User Context Isolation**
- Each request gets its own HTTP client
- No data leakage between users
- Client closed immediately after request

### 2. **Standard Authentication Pattern**
- Uses industry-standard `Authorization: Bearer <token>` header
- Compatible with API gateways, proxies, and standard HTTP clients

### 3. **Token Encryption**
- Plain JWT stored/passed by users (simple)
- Encryption happens server-side before calling e-courts API
- Users don't need to handle encryption

## Token Encryption Details

### What Users See:
- **Plain JWT token** from `/auth/token`
- Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### What Happens Internally:
1. User passes plain JWT in header
2. API extracts plain JWT
3. Scraper functions receive plain JWT
4. JWT is encrypted using `encrypt_request(token)` 
5. Encrypted JWT sent to e-courts backend in Authorization header
6. E-courts backend decrypts and validates

### Encryption Function (utils/crypto_utils.py):
```python
# User's plain JWT token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Encrypted for e-courts API
encrypted = encrypt_request(token)

# Sent to e-courts as:
headers = {'Authorization': f'Bearer {encrypted}'}
```

## API Usage Examples

### 1. Generate Token
```bash
curl -X POST http://localhost:8000/auth/token
```

**Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated successfully. Use this token in Authorization header as 'Bearer <token>' for all API requests",
  "data": {
    "token": "eyJhbGc..."
  }
}
```

### 2. Use Token in Requests
```bash
# Get States
curl -X GET http://localhost:8000/court/states \
  -H "Authorization: Bearer eyJhbGc..."

# Get Districts
curl -X POST http://localhost:8000/court/districts \
  -H "Authorization: Bearer eyJhbGc..." \
  -H "Content-Type: application/json" \
  -d '{"state_code": "1"}'

# Get Case Details
curl -X GET "http://localhost:8000/cases/details?cnr=DLHC010123452024" \
  -H "Authorization: Bearer eyJhbGc..."
```

## Error Handling

### Missing Token
**Request:** No Authorization header
**Response:** 401 - "Authorization header is required..."

### Invalid Format
**Request:** `Authorization: InvalidFormat token`
**Response:** 401 - "Invalid authorization header format..."

### Expired/Invalid Token
**Request:** Valid format but invalid/expired token
**Response:** 401 - "Request unauthorised..."

## Testing

Created `test_jwt_workflow.py` to validate:
1. ✅ Token generation
2. ✅ Request rejection without token
3. ✅ Request success with valid token
4. ✅ Request rejection with invalid format
5. ✅ POST requests with token

**Run tests:**
```bash
python test_jwt_workflow.py
```

## Benefits

### For Users:
1. **Standard Pattern**: Uses familiar `Authorization: Bearer` pattern
2. **Token Control**: Users manage their own tokens
3. **Reusability**: Generate once, use multiple times
4. **Clear Errors**: Descriptive error messages for auth issues

### For System:
1. **Isolation**: Per-request clients prevent cross-user contamination
2. **Security**: Proper token validation and format checking
3. **Maintainability**: Standard patterns easy to understand/extend
4. **Resource Management**: Clients properly closed after each request

## Documentation

Created comprehensive guides:
- **JWT_WORKFLOW.md**: Complete workflow documentation with examples
- **test_jwt_workflow.py**: Interactive testing script
- This summary document

## Migration Path

### If you had existing clients:
1. Update to call `/auth/token` first
2. Store the returned token
3. Add `Authorization: Bearer <token>` header to all requests
4. Handle 401 errors by regenerating token

### Code Example:
```python
import httpx

# Step 1: Get token
client = httpx.Client()
response = client.post("http://localhost:8000/auth/token")
token = response.json()["data"]["token"]

# Step 2: Use token
headers = {"Authorization": f"Bearer {token}"}
response = client.get("http://localhost:8000/court/states", headers=headers)
states = response.json()
```

## Verification

All files compile without errors:
- ✅ api/dependencies.py
- ✅ api/main.py
- ✅ api/routers/auth.py
- ✅ api/routers/cases.py
- ✅ api/routers/cause_list.py
- ✅ test_jwt_workflow.py

Server runs with `--reload` flag, changes automatically applied.

## Next Steps (Optional Enhancements)

1. **Token Expiration**: Add token expiration time to response
2. **Token Refresh**: Implement refresh token mechanism
3. **Rate Limiting**: Add per-token rate limiting
4. **Token Caching**: Cache valid tokens temporarily
5. **Logging**: Add token usage analytics (anonymized)
6. **OpenAPI**: Update OpenAPI schema to show Authorization requirement

## Conclusion

✅ Successfully implemented secure, user-managed JWT authentication
✅ Per-request HTTP clients ensure user context isolation  
✅ Standard Authorization header pattern  
✅ Comprehensive documentation and testing  
✅ Backward compatible token encryption for e-courts backend

# Swagger UI Authentication - FIXED ✅

## Issue Analysis

### Problem
When users generated a token via `/auth/token` in Swagger UI and tried to use it in other endpoints like `/court/states`, they received:
```
"Authorization header is required"
```

Even though they had a valid token.

### Root Cause
FastAPI's Swagger UI needs explicit security scheme configuration to:
1. Show the 🔓 **Authorize** button
2. Capture the token from users
3. Automatically include it in the `Authorization` header for requests

**The security scheme was missing**, so Swagger UI didn't know how to handle authentication.

## Solution Implemented

### 1. Added HTTPBearer Security Scheme (`api/dependencies.py`)

```python
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Security scheme for Swagger UI
security = HTTPBearer(
    scheme_name="Bearer Token",
    description="Enter your JWT token (obtained from POST /auth/token endpoint)",
    auto_error=False
)
```

This creates:
- The 🔓 **Authorize** button in Swagger UI
- Automatic header injection for authenticated requests
- Proper OpenAPI schema documentation

### 2. Updated `get_auth_token` Dependency

**Before:**
```python
async def get_auth_token(authorization: Optional[str] = Header(None)) -> str:
    # Manually parsed Authorization header
    if not authorization:
        raise HTTPException(...)
    parts = authorization.split()
    token = parts[1]
    return token
```

**After:**
```python
async def get_auth_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    """Uses HTTPBearer security scheme - integrates with Swagger UI"""
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Use the 🔓 Authorize button in Swagger UI...",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials
```

**Benefits:**
- ✅ Automatic Bearer token extraction
- ✅ Swagger UI integration
- ✅ Proper `WWW-Authenticate` headers
- ✅ Cleaner code

### 3. Enhanced API Description (`api/main.py`)

```python
app = FastAPI(
    title="E-Courts API",
    description="""REST API for accessing Indian e-Courts data.
    
## Authentication

1. **Generate Token**: Call `POST /auth/token` to get a JWT token
2. **Authorize**: Click the 🔓 Authorize button (top right)
3. **Enter Token**: Paste your token in the value field (without 'Bearer' prefix)
4. **Use APIs**: All authenticated endpoints will now work
    """,
    version="1.0.0",
    lifespan=lifespan
)
```

## How to Use (Step-by-Step)

### In Swagger UI (http://localhost:8000/docs)

#### Step 1: Generate Token
1. Open `/auth/token` endpoint
2. Click "Try it out" → "Execute"
3. Copy the token from response:
   ```json
   {
     "data": {
       "token": "eyJhbGc..."  ← Copy this
     }
   }
   ```

#### Step 2: Authorize
1. Click the **🔓 Authorize** button (top-right corner)
2. Paste your token (without "Bearer" prefix)
3. Click "Authorize"
4. Click "Close"
5. Button changes to 🔒 (you're authorized!)

#### Step 3: Use Any Endpoint
1. Try any endpoint (e.g., GET /court/states)
2. Click "Try it out" → "Execute"
3. Token is automatically included in the request!

### Via cURL

```bash
# 1. Generate token
TOKEN=$(curl -X POST http://localhost:8000/auth/token | jq -r '.data.token')

# 2. Use token in requests
curl -X GET http://localhost:8000/court/states \
  -H "Authorization: Bearer $TOKEN"
```

### Via Python (httpx)

```python
import httpx

client = httpx.Client()

# 1. Generate token
response = client.post("http://localhost:8000/auth/token")
token = response.json()["data"]["token"]

# 2. Use token
headers = {"Authorization": f"Bearer {token}"}
response = client.get("http://localhost:8000/court/states", headers=headers)
print(response.json())
```

## Testing Results

### ✅ Without Token (Expected Failure)
```bash
$ curl -X GET http://localhost:8000/court/states

Response:
{
  "detail": "Authorization header is required. Use the 🔓 Authorize button in Swagger UI or include 'Authorization: Bearer <token>' header"
}
```

### ✅ With Valid Token (Success)
```bash
$ curl -X GET http://localhost:8000/court/states \
  -H "Authorization: Bearer eyJ0eXAi..."

Response:
{
  "status": "success",
  "code": 200,
  "message": "States retrieved successfully",
  "data": {...}
}
```

## Verification

All endpoints now properly handle authentication:

### Authentication
- ✅ POST `/auth/token` - No auth required (generates token)

### Court & Cause List
- ✅ GET `/court/states` - Requires token
- ✅ POST `/court/districts` - Requires token
- ✅ POST `/court/complex` - Requires token
- ✅ POST `/court/names` - Requires token
- ✅ POST `/court/cause-list` - Requires token

### Cases
- ✅ GET `/cases/details` - Requires token

### Public Endpoints
- ✅ GET `/health` - No auth required
- ✅ GET `/` - No auth required

## Common Issues & Solutions

### Issue: "Authorization header is required"
**Cause:** You haven't authorized in Swagger UI

**Solution:**
1. Generate token from `/auth/token`
2. Click 🔓 Authorize button
3. Paste token
4. Try request again

### Issue: "UnAuthorized" from e-courts backend
**Cause:** Token expired (e-courts tokens expire quickly, ~10 minutes)

**Solution:**
1. Generate a **fresh** token
2. Re-authorize with new token
3. Try request immediately

**Note:** This is an e-courts backend limitation, not our API issue.

### Issue: Token not working after authorization
**Cause:** Old token cached or expired

**Solution:**
1. Click 🔒 Authorize → Logout
2. Generate fresh token
3. Authorize again

## Technical Implementation

### Security Flow
```
1. User clicks 🔓 Authorize in Swagger UI
2. Enters token in dialog
3. Swagger UI stores token
4. For each request:
   - Swagger UI adds: Authorization: Bearer <token>
5. FastAPI HTTPBearer extracts token
6. get_auth_token() dependency validates
7. Token passed to endpoint
8. Endpoint calls e-courts API with encrypted token
```

### HTTPBearer vs Manual Header
**HTTPBearer Advantages:**
- ✅ Automatic Swagger UI integration
- ✅ Proper OpenAPI documentation
- ✅ Standard security schemes
- ✅ Better error messages
- ✅ Less code, fewer bugs

## Files Modified

1. ✅ `api/dependencies.py` - Added HTTPBearer security scheme
2. ✅ `api/main.py` - Enhanced API description with auth instructions
3. ✅ `SWAGGER_AUTH_GUIDE.md` - Comprehensive user guide
4. ✅ This file - Technical documentation

## Summary

✅ **Problem Solved**: Swagger UI now properly handles JWT authentication

✅ **User Experience**: Clear 🔓 Authorize button workflow

✅ **Developer Experience**: Standard HTTPBearer security scheme

✅ **All Endpoints**: Consistently enforce authentication

✅ **Documentation**: Clear guides for users and developers

The authentication system is now fully functional in both Swagger UI and programmatic access (cURL, Python, etc.)!

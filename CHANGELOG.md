# API Update - GET Endpoint for Case Details

## Summary of Changes

The case details endpoint has been updated from **POST to GET** to follow RESTful conventions.

### ✅ Changes Made

#### 1. **api/routers/cases.py**
- **Before**: `@router.post("/details")`
- **After**: `@router.get("/details")`
- Changed parameter from body request to query parameter
- Updated function signature:
  - **Before**: `get_case_details(request: CaseDetailRequest, ...)`
  - **After**: `get_case_details(cnr: str, ...)`
- All references to `request.cnr` updated to `cnr`

#### 2. **Removed Unused Import**
- Removed `CaseDetailRequest` from imports in `cases.py`
- Still available in `schemas.py` if needed in future

#### 3. **Documentation Updates**

**QUICK_REFERENCE.md**
- Updated endpoint from `POST /cases/details` to `GET /cases/details?cnr=...`
- Shows query parameter usage

**API_README.md**
- Updated endpoint documentation
- Changed curl example to GET request
- Changed Python requests example from POST to GET with params
- Added query parameter documentation

**IMPLEMENTATION_SUMMARY.md**
- Updated API endpoints table
- Updated file descriptions
- Updated curl usage examples

### 📋 New Endpoint Usage

#### cURL
```bash
# Get case details
curl http://localhost:8000/cases/details?cnr=UPBL060021142023
```

#### Python (requests)
```python
import requests

headers = {'Authorization': f'Bearer {token}'}
case_response = requests.get(
    'http://localhost:8000/cases/details',
    params={'cnr': 'UPBL060021142023'},
    headers=headers
)
print(case_response.json())
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        'http://localhost:8000/cases/details',
        params={'cnr': 'UPBL060021142023'},
        headers={'Authorization': f'Bearer {token}'}
    )
    print(response.json())
```

### 🔄 Backward Compatibility

This is a **breaking change** for clients using the old POST endpoint. All clients need to be updated to use:
- **Method**: GET (instead of POST)
- **Parameter**: Query string (`?cnr=value`) instead of JSON body

### ✨ Benefits of GET Request

1. **RESTful Compliance**: Read-only operations should use GET
2. **Cacheability**: GET requests can be cached by browsers and proxies
3. **Bookmarkable**: URL contains all parameters
4. **Simpler**: No request body needed for simple queries
5. **Security**: CNR in URL is easier to validate than in JSON body

### 📊 All Endpoints Summary

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/token` | Generate JWT token |
| **GET** | **`/cases/details`** | Get case details by CNR (**UPDATED**) |
| GET | `/court/states` | Get all states |
| POST | `/court/districts` | Get districts by state |
| POST | `/court/complex` | Get court complex |
| POST | `/court/names` | Get court names |
| POST | `/court/cause-list` | Get cause list |
| GET | `/health` | Health check |

### 🧪 Testing the Endpoint

#### Using Swagger UI
1. Go to http://localhost:8000/docs
2. Find the GET `/cases/details` endpoint
3. Click "Try it out"
4. Enter `cnr` value: `UPBL060021142023`
5. Click "Execute"

#### Using cURL
```bash
# First get a token
TOKEN=$(curl -s -X POST http://localhost:8000/auth/token | jq -r '.data.token')

# Then get case details
curl "http://localhost:8000/cases/details?cnr=UPBL060021142023" \
  -H "Authorization: Bearer $TOKEN"
```

---

**Status**: ✅ Complete
**Date**: October 16, 2025
**Breaking Change**: Yes - Update clients to use GET instead of POST

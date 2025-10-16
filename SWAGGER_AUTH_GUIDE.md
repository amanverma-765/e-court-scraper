# Swagger UI Authentication Guide

## How to Use JWT Authentication in Swagger UI

### Step 1: Generate a Token

1. Navigate to **Swagger UI**: http://localhost:8000/docs
2. Scroll down to the **Authentication** section
3. Click on **POST /auth/token** endpoint
4. Click **"Try it out"** button
5. Click **"Execute"** button
6. Copy the token from the response (under `data.token`)

**Example Response:**
```json
{
  "status": "success",
  "code": 200,
  "message": "Token generated successfully...",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."  ← Copy this
  }
}
```

### Step 2: Authorize in Swagger UI

1. Look for the **🔓 Authorize** button (top right of the page)
2. Click the **🔓 Authorize** button
3. A dialog box will appear
4. **Paste your token** in the "Value" field
   - ⚠️ **DO NOT include "Bearer"** - just paste the token directly
   - Example: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
5. Click **"Authorize"** button
6. Click **"Close"** to dismiss the dialog

**What happens:**
- The 🔓 icon will change to 🔒 (indicating you're authorized)
- All subsequent API requests will automatically include the Authorization header

### Step 3: Use Protected Endpoints

Now you can test any endpoint! For example:

1. Go to **GET /court/states** endpoint
2. Click **"Try it out"**
3. Click **"Execute"**
4. The request will automatically include your token in the header

**Behind the scenes:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Visual Guide

```
┌─────────────────────────────────────────────────────────────┐
│  Swagger UI (http://localhost:8000/docs)                    │
├─────────────────────────────────────────────────────────────┤
│                                           🔓 Authorize       │  ← Click this
│                                                              │
│  Authentication                                              │
│  ▼ POST /auth/token  [Try it out]                          │  ← Step 1: Generate token
│    [Execute]                                                 │
│    Response:                                                 │
│    {                                                         │
│      "data": {                                              │
│        "token": "eyJhbGc..."  ← Copy this                   │
│      }                                                       │
│    }                                                         │
│                                                              │
│  ┌────────────────────────────────────────────┐            │
│  │ Available authorizations                    │            │  ← Step 2: Paste token here
│  │                                             │            │
│  │ Bearer Token (http, Bearer)                │            │
│  │ Value: [eyJhbGc...]                        │            │  ← Just the token (no "Bearer")
│  │                                             │            │
│  │          [Authorize]  [Close]              │            │  ← Click Authorize
│  └────────────────────────────────────────────┘            │
│                                           🔒 Authorize       │  ← Icon changes
│                                                              │
│  Court & Cause List                                         │
│  ▼ GET /court/states  [Try it out]                         │  ← Step 3: Use any endpoint
│    [Execute]                                                 │  ← Works automatically!
└─────────────────────────────────────────────────────────────┘
```

### Troubleshooting

#### Issue: "Authorization header is required"
**Problem:** You haven't authorized or the token expired

**Solution:**
1. Generate a new token from POST /auth/token
2. Click 🔒 Authorize button (top right)
3. Paste the new token
4. Try your request again

#### Issue: "Invalid authorization header format"
**Problem:** You included "Bearer" in the value field

**Solution:**
- ❌ Wrong: `Bearer eyJhbGc...`
- ✅ Correct: `eyJhbGc...`

Just paste the token value directly.

#### Issue: Token not working after authorizing
**Problem:** The token might be expired or invalid

**Solution:**
1. Click the 🔒 Authorize button
2. Click **"Logout"** to clear old token
3. Generate a fresh token from POST /auth/token
4. Authorize again with the new token

### Testing Multiple Endpoints

Once authorized, you can test any endpoint without re-authorizing:

1. ✅ GET /court/states
2. ✅ POST /court/districts  
3. ✅ POST /court/complex
4. ✅ POST /court/names
5. ✅ POST /court/cause-list
6. ✅ GET /cases/details

All will automatically include your token!

### Logout

To clear your authorization:
1. Click the 🔒 Authorize button
2. Click **"Logout"** next to Bearer Token
3. Click **"Close"**
4. Icon changes back to 🔓

### Using cURL from Swagger

After executing a request, you can copy the cURL command:

1. Execute any endpoint
2. Look for **"Copy cURL"** button in the response section
3. The generated cURL will include your Authorization header

Example:
```bash
curl -X 'GET' \
  'http://localhost:8000/court/states' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGc...'
```

## Testing Workflow Summary

1. **Generate Token**: POST /auth/token → Copy token
2. **Authorize**: Click 🔓 → Paste token → Authorize
3. **Test Endpoints**: All endpoints now work automatically
4. **Logout/Re-authorize**: If token expires, generate new token and authorize again

## Common Mistakes

### ❌ Including "Bearer" in the authorization dialog
```
Value: Bearer eyJhbGc...  ← Wrong!
```

### ✅ Just the token
```
Value: eyJhbGc...  ← Correct!
```

### ❌ Trying to use endpoints without authorizing first
- Always click 🔓 Authorize after generating a token

### ❌ Using an expired or old token
- Generate a fresh token if you get 401 errors

## Technical Details

When you authorize in Swagger UI:
- FastAPI's `HTTPBearer` security scheme is activated
- Your token is stored in the browser session
- Every request automatically adds: `Authorization: Bearer <your-token>`
- The `get_auth_token` dependency extracts and validates the token
- If valid, the request proceeds; if invalid, you get a 401 error

## Need Help?

If authorization isn't working:
1. Check browser console for errors (F12)
2. Verify the token was generated successfully
3. Make sure you clicked "Authorize" button
4. Try logging out and authorizing again
5. Generate a fresh token if issues persist

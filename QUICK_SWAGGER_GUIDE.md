# Quick Reference: Using Swagger UI with JWT Authentication

## TL;DR - 3 Simple Steps

### 1️⃣ Generate Token
```
POST /auth/token → Copy token from response
```

### 2️⃣ Authorize
```
Click 🔓 button → Paste token → Authorize → Close
```

### 3️⃣ Use Endpoints
```
All endpoints now work automatically! 🎉
```

---

## Visual Quick Guide

```
┌──────────────────────────────────────┐
│  Swagger UI                          │
│                    🔓 Authorize ←─── Click here (Step 2)
│                                      │
│  📁 Authentication                   │
│  POST /auth/token ←───────────────── Use this first (Step 1)
│  [Try it out] [Execute]              │
│  Response: {"data":{"token":"..."}} ←─ Copy token
│                                      │
│  📁 Court & Cause List               │
│  GET /court/states ←─────────────── Now works! (Step 3)
│  [Try it out] [Execute]              │
└──────────────────────────────────────┘
```

## The Authorization Dialog

When you click 🔓 Authorize:

```
┌────────────────────────────────────┐
│ Available authorizations           │
│                                    │
│ Bearer Token (http, Bearer)       │
│                                    │
│ Value: [Paste token here]         │ ← Just the token, no "Bearer"
│                                    │
│     [Authorize]    [Close]         │
└────────────────────────────────────┘
```

## Common Mistakes

### ❌ Wrong
```
Value: Bearer eyJ0eXA...
```

### ✅ Correct  
```
Value: eyJ0eXA...
```

---

## Token Expiry

⚠️ **E-courts tokens expire quickly (~10 minutes)**

If you get "UnAuthorized" error:
1. Generate new token from POST /auth/token
2. Click 🔒 → Logout → Re-authorize with new token

---

## Need Help?

See detailed guides:
- 📖 `SWAGGER_AUTH_GUIDE.md` - Comprehensive guide
- 📖 `SWAGGER_FIX_SUMMARY.md` - Technical details
- 📖 `JWT_WORKFLOW.md` - Complete JWT workflow

---

## Quick Test

Try this right now:

1. Open: http://localhost:8000/docs
2. POST /auth/token → Execute → Copy token
3. Click 🔓 → Paste token → Authorize
4. GET /court/states → Execute
5. See states data! ✅

That's it! 🚀

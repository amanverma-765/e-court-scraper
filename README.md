# E-Courts API

High-performance REST API for accessing Indian e-Courts data with JWT authentication.

## Why This API?

- ⚡ **Blazing Fast** - Direct API calls, no browser overhead
- � **No CAPTCHA** - Bypasses CAPTCHA requirements entirely
- 🤖 **No Bot Detection** - Native HTTP requests, undetectable
- � **No Rate Limits** - Fetch data without restrictions
- 🔒 **Secure** - JWT authentication with per-request isolation
- � **Complete Data Access** - States, districts, courts, cause lists, case details
- 🛡️ **Better Error Handling** - Clear error messages and status codes
- 📚 **Interactive Docs** - Built-in Swagger UI for easy testing

## Installation & Setup

### Option 1: Using uv (Recommended ⚡)

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package installer and resolver.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup
git clone https://github.com/amanverma-765/e-court-scraper.git
cd e-court-scraper

# Install dependencies
uv sync

# Run the API (choose one method):

# Method 1: Using justfile (requires just: https://github.com/casey/just)
just run

# Method 2: Using the startup script
./start.sh

# Method 3: Direct uvicorn command
uv run uvicorn api.main:app --reload

# Method 4: Run as Python module
uv run python -m api.main
```

### Option 2: Using pip

```bash
# Clone and install
git clone https://github.com/amanverma-765/e-court-scraper.git
cd e-court-scraper
pip install -r requirements.txt

# Run the API (choose one method):

# Method 1: Using justfile (requires just)
just run

# Method 2: Using the startup script
./start.sh

# Method 3: Direct uvicorn command
uvicorn api.main:app --reload

# Method 4: Run as Python module
python -m api.main
```

API will be available at: **http://localhost:8000**

## Quick Example

```bash
# 1. Generate token
curl -X POST http://localhost:8000/auth/token

# 2. Use token to fetch data
TOKEN="your_token_here"
curl -X GET "http://localhost:8000/court/states" \
  -H "Authorization: Bearer $TOKEN"
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/auth/token` | POST | Generate JWT token |
| `/court/states` | GET | Get all states |
| `/court/districts` | POST | Get districts by state |
| `/court/complex` | POST | Get court complexes |
| `/court/names` | POST | Get court names |
| `/court/cause-list` | POST | Get cause list |
| `/cases/details` | GET | Get case details by CNR |

**📖 Complete Documentation:** See [API_DOCS.md](API_DOCS.md) for detailed request/response examples, error handling, and code samples.

**🎯 Interactive Testing:** Visit http://localhost:8000/docs for Swagger UI

## Technical Advantages

### Performance
- **Native HTTP Requests** - Uses `httpx` for direct API communication
- **No Browser Required** - No Selenium, Playwright, or headless browsers
- **Faster Than Scraping** - 10x faster than traditional web scraping methods
- **Concurrent Requests** - Handle multiple requests simultaneously

### Security & Reliability
- **CAPTCHA Bypass** - Direct API access eliminates CAPTCHA challenges
- **No Bot Detection** - Mimics legitimate e-courts mobile app requests
- **Automatic Encryption** - Handles AES encryption/decryption transparently
- **Token Management** - Automatic token generation and validation

### Developer Experience
- **Clean REST API** - Standard HTTP methods and JSON responses
- **OpenAPI/Swagger** - Auto-generated interactive documentation
- **Type Safety** - Pydantic models for request/response validation
- **Better Error Messages** - Clear error codes and actionable messages

## Requirements

- Python 3.10+
- Dependencies: `fastapi`, `httpx`, `uvicorn`, `pycryptodome`

See `requirements.txt` for complete list.

## Notes

- **Token Expiry**: Tokens expire after ~10 minutes. Generate fresh tokens on 401 errors.
- **Data Format**: Some endpoints return HTML or special formatted strings. See API_DOCS.md for parsing details.

## Disclaimer

Not officially affiliated with e-Courts India. For educational and research purposes only.

## Links

- 📖 **[Complete API Documentation](API_DOCS.md)** - Request/response examples, error handling
- 🐛 **[Report Issues](https://github.com/amanverma-765/e-court-scraper/issues)**
- 💡 **[Feature Requests](https://github.com/amanverma-765/e-court-scraper/issues/new)**

---

**Built with FastAPI** | **Powered by httpx**

"""
Main FastAPI application entry point.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.routers import auth as auth_routes
from api.routers import cases as cases_routes
from api.routers import cause_list as cause_list_routes
from api.exceptions import register_exception_handlers
from api.schemas import HealthCheckResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown.
    """
    # Startup
    logger.info("E-Courts API starting up")
    logger.info("Using per-request HTTP clients for user isolation")
    
    yield
    
    # Shutdown
    logger.info("E-Courts API shutting down")


# Create FastAPI application
app = FastAPI(
    title="E-Courts API",
    description="""REST API for accessing Indian e-Courts data.
    
## Authentication

1. **Generate Token**: Call `POST /auth/token` to get a JWT token
2. **Authorize**: Click the 🔓 Authorize button (top right)
3. **Enter Token**: Paste your token in the value field (without 'Bearer' prefix)
4. **Use APIs**: All authenticated endpoints will now work

The token will be automatically included in the `Authorization: Bearer <token>` header.
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure as per your requirements
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "app.ecourts.gov.in"]
)

# Register exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(auth_routes.router)
app.include_router(cases_routes.router)
app.include_router(cause_list_routes.router)


@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Health"],
    summary="Health Check",
    description="Check if the API is running and healthy"
)
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "message": "API is running"
    }


# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Welcome to E-Courts API"
)
async def root() -> dict:
    """
    Root endpoint providing API information.
    
    Returns:
        dict: API information
    """
    return {
        "message": "Welcome to E-Courts API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi_schema": "/openapi.json"
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

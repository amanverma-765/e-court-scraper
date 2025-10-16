import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from api.routers import auth as auth_routes
from api.routers import cases as cases_routes
from api.routers import cause_list as cause_list_routes
from api.exceptions import register_exception_handlers
from api.schemas import HealthCheckResponse

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("E-Courts API starting up")
    yield
    logger.info("E-Courts API shutting down")


app = FastAPI(
    title="E-Courts API",
    description="REST API for Indian e-Courts data. Get token from /auth/token, then use 🔓 Authorize button.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "app.ecourts.gov.in"]
)

register_exception_handlers(app)

app.include_router(auth_routes.router)
app.include_router(cases_routes.router)
app.include_router(cause_list_routes.router)


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check() -> dict:
    return {"status": "healthy", "message": "API is running"}


@app.get("/", tags=["Root"])
async def root() -> dict:
    return {
        "message": "Welcome to E-Courts API",
        "version": "1.0.0",
        "docs": "/docs"
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

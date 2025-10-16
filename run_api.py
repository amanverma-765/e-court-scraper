#!/usr/bin/env python
"""
Quick start guide for running the E-Courts API.

This script demonstrates how to start the API server.
"""

import subprocess
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required packages are installed."""
    required_packages = [
        'fastapi',
        'uvicorn',
        'httpx',
        'pydantic',
        'pycryptodome'
    ]
    
    logger.info("Checking dependencies...")
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✓ {package} is installed")
        except ImportError:
            logger.warning(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.info("Install with: pip install -r requirements.txt")
        return False
    
    logger.info("All dependencies are installed!")
    return True


def start_api(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Start the FastAPI server."""
    logger.info(f"Starting E-Courts API on {host}:{port}")
    
    # Build uvicorn command
    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        "api.main:app",
        "--host", host,
        "--port", str(port),
    ]
    
    if reload:
        cmd.append("--reload")
        logger.info("Auto-reload enabled (development mode)")
    else:
        logger.info("Running in production mode")
    
    logger.info(f"Starting command: {' '.join(cmd)}")
    logger.info("=" * 60)
    logger.info("API Documentation: http://localhost:8000/docs")
    logger.info("ReDoc: http://localhost:8000/redoc")
    logger.info("=" * 60)
    
    try:
        subprocess.run(cmd, check=False)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Start the E-Courts API server"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind to (default: 8000)"
    )
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload (production mode)"
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("E-Courts API - Startup Script")
    logger.info("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        logger.error("Please install missing dependencies")
        sys.exit(1)
    
    # Start API
    start_api(
        host=args.host,
        port=args.port,
        reload=not args.no_reload
    )


if __name__ == "__main__":
    main()

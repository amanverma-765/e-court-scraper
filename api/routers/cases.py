"""
Case-related routes for the API.
"""

import logging
import httpx
from fastapi import APIRouter, Depends, status

from scraper.case_manager import get_details_by_cnr
from api.schemas import (
    CaseDetailResponse,
    ErrorResponse
)
from api.dependencies import get_http_client, get_auth_token
from utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
    NotFoundException
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get(
    "/details",
    response_model=CaseDetailResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Case not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get Case Details by CNR",
    description="Retrieve detailed information about a case using its Case Number Reference (CNR)"
)
async def get_case_details(
    cnr: str,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve case details by CNR.
    
    Args:
        cnr: Case Number Reference (query parameter)
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: Case details
        
    Raises:
        UnauthorizedException: If authentication fails
        BadRequestException: If request is invalid
        NotFoundException: If case is not found
    """
    try:
        logger.info(f"Fetching case details for CNR: {cnr}")
        
        details = get_details_by_cnr(client, token, cnr)
        
        logger.info(f"Case details retrieved successfully for CNR: {cnr}")
        return {
            "status": "success",
            "code": 200,
            "message": "Case details retrieved successfully",
            "data": details
        }
        
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed for CNR {cnr}: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"Case not found for CNR {cnr}: {e}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request for CNR {cnr}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching case details for CNR {cnr}: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()

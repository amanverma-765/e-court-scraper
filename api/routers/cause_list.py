"""
Cause list and court-related routes for the API.
"""

import logging
import httpx
from fastapi import APIRouter, Depends, status

from scraper.cause_list_manager import (
    get_states,
    get_districts,
    get_court_complex,
    get_court_name,
    get_cause_list
)
from api.schemas import (
    StatesResponse,
    DistrictsRequest,
    DistrictsResponse,
    CourtComplexRequest,
    CourtComplexResponse,
    CourtNameRequest,
    CourtNameResponse,
    CauseListRequest,
    CauseListResponse,
    ErrorResponse
)
from api.dependencies import get_http_client, get_auth_token
from utils.cause_list_type import CauseListType
from utils.exceptions import (
    UnauthorizedException,
    BadRequestException,
    NotFoundException
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/court", tags=["Court & Cause List"])


@router.get(
    "/states",
    response_model=StatesResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Data not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get List of States",
    description="Retrieve list of all states available in e-courts system"
)
async def fetch_states(
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve list of states.
    
    Args:
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: List of states
        
    Raises:
        UnauthorizedException: If authentication fails
        NotFoundException: If data is not found
    """
    try:
        logger.info("Fetching states list")
        states = get_states(client, token)
        
        logger.info("States list retrieved successfully")
        return {
            "status": "success",
            "code": 200,
            "message": "States retrieved successfully",
            "data": states
        }
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"States data not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching states: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()


@router.post(
    "/districts",
    response_model=DistrictsResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Data not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get Districts by State",
    description="Retrieve list of districts for a given state code"
)
async def fetch_districts(
    request: DistrictsRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve districts for a state.
    
    Args:
        request: Request containing state code
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: List of districts
        
    Raises:
        UnauthorizedException: If authentication fails
        BadRequestException: If request is invalid
        NotFoundException: If data is not found
    """
    try:
        logger.info(f"Fetching districts for state: {request.state_code}")
        districts = get_districts(client, token, request.state_code)
        
        logger.info(f"Districts retrieved successfully for state: {request.state_code}")
        return {
            "status": "success",
            "code": 200,
            "message": "Districts retrieved successfully",
            "data": districts
        }
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed: {e}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"Districts not found for state {request.state_code}: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching districts for state {request.state_code}: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()


@router.post(
    "/complex",
    response_model=CourtComplexResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Data not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get Court Complex",
    description="Retrieve court complex information for a state and district"
)
async def fetch_court_complex(
    request: CourtComplexRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve court complex.
    
    Args:
        request: Request containing state and district codes
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: Court complex data
        
    Raises:
        UnauthorizedException: If authentication fails
        BadRequestException: If request is invalid
        NotFoundException: If data is not found
    """
    try:
        logger.info(f"Fetching court complex for state: {request.state_code}, district: {request.district_code}")
        complex_data = get_court_complex(client, token, request.state_code, request.district_code)
        
        logger.info(f"Court complex retrieved successfully")
        return {
            "status": "success",
            "code": 200,
            "message": "Court complex retrieved successfully",
            "data": complex_data
        }
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed: {e}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"Court complex not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching court complex: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()


@router.post(
    "/names",
    response_model=CourtNameResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Data not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get Court Names",
    description="Retrieve list of court names for a given state, district, and court code"
)
async def fetch_court_names(
    request: CourtNameRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve court names.
    
    Args:
        request: Request containing state, district, and court codes
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: List of court names
        
    Raises:
        UnauthorizedException: If authentication fails
        BadRequestException: If request is invalid
        NotFoundException: If data is not found
    """
    try:
        logger.info(f"Fetching court names for state: {request.state_code}, district: {request.district_code}, court: {request.court_code}")
        names = get_court_name(client, token, request.state_code, request.district_code, request.court_code)
        
        logger.info(f"Court names retrieved successfully")
        return {
            "status": "success",
            "code": 200,
            "message": "Court names retrieved successfully",
            "data": names
        }
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed: {e}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"Court names not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching court names: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()


@router.post(
    "/cause-list",
    response_model=CauseListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Data not found"},
        500: {"model": ErrorResponse, "description": "Internal server error"},
    },
    summary="Get Cause List",
    description="Retrieve cause list for a specific court, date, and type (CIVIL or CRIMINAL)"
)
async def fetch_cause_list(
    request: CauseListRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    """
    Retrieve cause list.
    
    Args:
        request: Request containing court details, date, and type
        token: JWT authentication token
        client: HTTP client for making requests
        
    Returns:
        dict: Cause list data
        
    Raises:
        UnauthorizedException: If authentication fails
        BadRequestException: If request is invalid
        NotFoundException: If data is not found
    """
    try:
        # Convert cause list type string to enum
        cause_type = CauseListType[request.cause_list_type.upper()]
        
        logger.info(f"Fetching cause list for state: {request.state_code}, district: {request.district_code}, "
                   f"court: {request.court_code}, date: {request.date}, type: {request.cause_list_type}")
        
        cause_list = get_cause_list(
            client,
            token,
            request.state_code,
            request.district_code,
            request.court_code,
            request.court_number,
            cause_type,
            request.date
        )
        
        logger.info(f"Cause list retrieved successfully for {request.cause_list_type}")
        return {
            "status": "success",
            "code": 200,
            "message": "Cause list retrieved successfully",
            "data": cause_list
        }
    except KeyError:
        logger.warning(f"Invalid cause list type: {request.cause_list_type}")
        raise BadRequestException(f"Invalid cause list type. Must be 'CIVIL' or 'CRIMINAL'")
    except UnauthorizedException as e:
        logger.warning(f"Authorization failed: {e}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request: {e}")
        raise
    except NotFoundException as e:
        logger.warning(f"Cause list not found: {e}")
        raise
    except Exception as e:
        logger.error(f"Error fetching cause list: {e}", exc_info=True)
        raise
    finally:
        # Close the client after use since it's per-request
        client.close()

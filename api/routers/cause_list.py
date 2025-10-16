import logging
import httpx
from fastapi import APIRouter, Depends, status

from scraper.cause_list_manager import (
    get_states, get_districts, get_court_complex, get_court_name, get_cause_list
)
from api.schemas import (
    StatesResponse, DistrictsRequest, DistrictsResponse,
    CourtComplexRequest, CourtComplexResponse,
    CourtNameRequest, CourtNameResponse,
    CauseListRequest, CauseListResponse, ErrorResponse
)
from api.dependencies import get_http_client, get_auth_token
from utils.cause_list_type import CauseListType
from utils.exceptions import UnauthorizedException, BadRequestException, NotFoundException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/court", tags=["Court & Cause List"])


@router.get(
    "/states",
    response_model=StatesResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Get States"
)
async def fetch_states(
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        states = get_states(client, token)
        return {
            "status": "success",
            "code": 200,
            "message": "States retrieved",
            "data": states
        }
    except (UnauthorizedException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Error fetching states: {e}")
        raise
    finally:
        client.close()


@router.post(
    "/districts",
    response_model=DistrictsResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get Districts by State"
)
async def fetch_districts(
    request: DistrictsRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        districts = get_districts(client, token, request.state_code)
        return {
            "status": "success",
            "code": 200,
            "message": "Districts retrieved",
            "data": districts
        }
    except (UnauthorizedException, BadRequestException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Error fetching districts: {e}")
        raise
    finally:
        client.close()


@router.post(
    "/complex",
    response_model=CourtComplexResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get Court Complex"
)
async def fetch_court_complex(
    request: CourtComplexRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        complex_data = get_court_complex(client, token, request.state_code, request.district_code)
        return {
            "status": "success",
            "code": 200,
            "message": "Court complex retrieved",
            "data": complex_data
        }
    except (UnauthorizedException, BadRequestException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Error fetching court complex: {e}")
        raise
    finally:
        client.close()


@router.post(
    "/names",
    response_model=CourtNameResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get Court Names"
)
async def fetch_court_names(
    request: CourtNameRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        names = get_court_name(client, token, request.state_code, request.district_code, request.court_code)
        return {
            "status": "success",
            "code": 200,
            "message": "Court names retrieved",
            "data": names
        }
    except (UnauthorizedException, BadRequestException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Error fetching court names: {e}")
        raise
    finally:
        client.close()


@router.post(
    "/cause-list",
    response_model=CauseListResponse,
    status_code=status.HTTP_200_OK,
    responses={400: {"model": ErrorResponse}, 401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Get Cause List"
)
async def fetch_cause_list(
    request: CauseListRequest,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        cause_type = CauseListType[request.cause_list_type.upper()]
        cause_list = get_cause_list(
            client, token, request.state_code, request.district_code,
            request.court_code, request.court_number, cause_type, request.date
        )
        return {
            "status": "success",
            "code": 200,
            "message": "Cause list retrieved",
            "data": cause_list
        }
    except KeyError:
        raise BadRequestException("Invalid cause list type. Must be 'CIVIL' or 'CRIMINAL'")
    except (UnauthorizedException, BadRequestException, NotFoundException):
        raise
    except Exception as e:
        logger.error(f"Error fetching cause list: {e}")
        raise
    finally:
        client.close()

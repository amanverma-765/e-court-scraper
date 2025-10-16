import logging
import httpx
from fastapi import APIRouter, Depends, status

from scraper.case_manager import get_details_by_cnr
from api.schemas import CaseDetailResponse, ErrorResponse
from api.dependencies import get_http_client, get_auth_token
from utils.exceptions import UnauthorizedException, BadRequestException, NotFoundException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get(
    "/details",
    response_model=CaseDetailResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
    summary="Get Case Details by CNR"
)
async def get_case_details(
    cnr: str,
    token: str = Depends(get_auth_token),
    client: httpx.Client = Depends(get_http_client)
) -> dict:
    try:
        details = get_details_by_cnr(client, token, cnr)
        return {
            "status": "success",
            "code": 200,
            "message": "Case details retrieved",
            "data": details
        }
    except (UnauthorizedException, NotFoundException, BadRequestException):
        raise
    except Exception as e:
        logger.error(f"Error fetching case {cnr}: {e}")
        raise
    finally:
        client.close()

import logging
import time
import urllib.parse
from typing import Any

from httpx import Client
from utils.constants import BASE_URL
from utils.crypto_utils import encrypt_request, decrypt_response
from utils.exceptions import UnauthorizedException, BadRequestException, NotFoundException

logger = logging.getLogger(__name__)

def get_states(
        client: Client,
        token: str
) -> dict:
    body = {
        'action_code': 'fillState',
        'time': str(time.time())
    }
    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/stateWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting case detail by cnr: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No state data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"States retrieved successfully: {data}")
    return data


def get_districts(
        client: Client,
        token: str
) -> dict:
    body = {
        'action_code': 'fillState',
        'time': str(time.time())
    }
    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/stateWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting case detail by cnr: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No state data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"States retrieved successfully: {data}")
    return data
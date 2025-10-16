import logging
import time
import urllib.parse

from httpx import Client

from utils.cause_list_type import CauseListType
from utils.constants import BASE_URL, DEVICE_ID
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
        raise BadRequestException(f"Error getting states data: {response.status_code}: {response.text}")

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
        token: str,
        state_code: str
) -> dict:
    body = {
        'state_code': state_code,
        'test_param': 'pending'
    }

    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/districtWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting district data: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No district data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Districts retrieved successfully: {data}")
    return data


def get_court_complex(
        client: Client,
        token: str,
        state_code: str,
        district_code: str,
) -> dict:
    body = {
        'action_code': 'fillCourtComplex',
        'state_code': state_code,
        'dist_code': district_code
    }

    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/courtEstWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting court complex data: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No court complex data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Court complex retrieved successfully: {data}")
    return data


def get_court_name(
        client: Client,
        token: str,
        state_code: str,
        district_code: str,
        court_code: str
) -> dict:
    body = {
        'state_code': state_code,
        'dist_code': district_code,
        'court_code': court_code,
        'language_flag': 'english',
        'bilingual_flag': '0'
    }

    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/courtNameWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting court name data: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No court name data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Court names retrieved successfully: {data}")
    return data


def get_cause_list(
        client: Client,
        token: str,
        state_code: str,
        district_code: str,
        court_code: str,
        court_number: str,
        type: CauseListType,
        date: str
) -> dict:
    body = {
        'state_code': state_code,
        'dist_code': district_code,
        'flag': type.value,
        # 1 if Selected date is today or in the future (current/upcoming dates)
        # 0 if Selected date is in the past (previous dates)
        'selprevdays': "0",
        'court_no': court_number,
        'court_code': court_code,
        'causelist_date': date,
        'language_flag': 'english',
        'bilingual_flag': '0',
        'uid': f'{DEVICE_ID}:in.gov.ecourts.eCourtsServices'
    }

    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)
    response = client.get(
        f"{BASE_URL}/cases_new.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting cause list data: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No cause list data found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    try:
        data = decrypt_response(response.text)
        logger.info(f"Cause list retrieved successfully: {data}")
        return data
    except(ValueError, KeyError) as e:
        raise BadRequestException(f"You can only get 30 days of data: {response.status_code}: {response.text}")

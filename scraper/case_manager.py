import logging
import urllib.parse
from httpx import Client

from utils.constants import BASE_URL
from utils.crypto_utils import encrypt_request, decrypt_response
from utils.exceptions import UnauthorizedException, BadRequestException, NotFoundException

logger = logging.getLogger(__name__)


def get_details_by_cnr(
        client: Client,
        token: str,
        cnr: str
) -> dict:
    try:
        logger.info(f"Getting details for CNR: {cnr}")
        case_list = get_case_list(client, token, cnr)
        if case_list.get("case_number") is None:
            logger.info("Retrieving filling case details for CNR")
            details = get_filling_case_details(client, token, cnr)
            return details
        else:
            logger.info("Retrieving default case details for CNR")
            details = get_default_case_details(client, token, cnr)
            return details

    except UnauthorizedException as ue:
        raise ue
    except Exception as e:
        logger.error(f"Failed to get case details by CNR: {e}")
        raise e


def get_default_case_details(
        client: Client,
        token: str,
        cnr: str
) -> dict:
    body = {
        'cinum': cnr,
        'language_flag': 'english',
        'bilingual_flag': '0'
    }
    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)

    response = client.get(
        f"{BASE_URL}/caseHistoryWebService.php?params={encoded_body}",
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
        raise NotFoundException("No case details found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Default Case details retrieved by cnr: {data}")
    return data


def get_filling_case_details(
        client: Client,
        token: str,
        cnr: str
) -> dict:
    body = {
        'cino': cnr,
        'language_flag': 'english',
        'bilingual_flag': '0'
    }
    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)

    response = client.get(
        f"{BASE_URL}/filingCaseHistory.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting filling case detail by cnr: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No case details found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Default Case details retrieved by cnr: {data}")
    return data


def get_case_list(
        client: Client,
        token: str,
        cnr: str
) -> dict:
    body = {
        'cino': cnr,
        'version_number': '3.0',
        'language_flag': 'english',
        'bilingual_flag': '0'
    }
    enc_body = encrypt_request(body)
    encoded_body = urllib.parse.quote(enc_body)

    response = client.get(
        f"{BASE_URL}/listOfCasesWebService.php?params={encoded_body}",
        headers={
            'Authorization': f'Bearer {encrypt_request(token)}'
        }
    )

    if response.status_code == 401 or response.status_code == 403:
        raise UnauthorizedException(f"Request unauthorised: {response.text}")
    elif response.status_code != 200:
        raise BadRequestException(f"Error getting filling case detail by cnr: {response.status_code}: {response.text}")

    try:
        response.json()
        raise NotFoundException("No case list found")
    except (ValueError, KeyError) as e:
        # If JSON parsing fails, assume it's encrypted data
        pass

    data = decrypt_response(response.text)
    logger.info(f"Default Case details retrieved by cnr: {data}")
    return data

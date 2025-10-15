import logging
import urllib.parse

from httpx import Client

from utils.constants import DEVICE_ID, BASE_URL
from utils.crypto_utils import encrypt_request, decrypt_response

logger = logging.getLogger(__name__)

def get_jwt_token(client: Client) -> str | None:
    """Fetch JWT token from API."""
    try:
        body = {"version": "3.0", "uid": f"{DEVICE_ID}:in.gov.ecourts.eCourtsServices"}
        enc_body = encrypt_request(body)
        encoded_body = urllib.parse.quote(enc_body)

        response = client.get(
            url=f"{BASE_URL}/appReleaseWebService.php?params={encoded_body}",
            timeout=30
        )

        if response.status_code != 200:
            logger.error(f"Auth failed: HTTP {response.status_code}")
            return None

        dec_response = decrypt_response(response.text)
        jwt_token = dec_response.get("token")

        if not jwt_token:
            logger.error("Token missing in response")
            return None

        logger.info(f"Generated JWT token: {jwt_token}")
        return jwt_token

    except Exception as e:
        logger.error(f"Auth failed: {e}")
        return None
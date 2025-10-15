import logging

import httpx

from scraper.auth_manager import get_jwt_token


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


header = {
    "Host": "app.ecourts.gov.in",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 16; Pixel 7 Build/BP3A.250905.014)",
    "Accept-Encoding": "gzip",
    "Accept-Charset": "UTF-8",
    "Connection": "keep-alive",
}

def main():
    try:
        with httpx.Client(headers=header, timeout=20, follow_redirects=True) as client:
            print("Fetching JWT token...")
            token = get_jwt_token(client)
            if token is None:
                logger.error("Failed to fetch auth token, try again.")
                return


    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
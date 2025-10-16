import logging

import httpx

from scraper.auth_manager import get_jwt_token
from scraper.case_manager import get_details_by_cnr
from scraper.cause_list_manager import get_states, get_districts, get_court_complex, get_court_name, get_cause_list
from utils.cause_list_type import CauseListType

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

            # get_details_by_cnr(client, token, "UPBL060021142023")
            # get_states(client, token)
            # get_districts(client, token, "5")
            # get_court_complex(client, token, "5", "7")
            # get_court_name(client, token, "5", "7", "3")
            get_cause_list(client, token, "5", "7", "1", "1", CauseListType.CIVIL, "16-10-2020")

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
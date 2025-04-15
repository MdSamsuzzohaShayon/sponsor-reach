# crm/sync_crm.py

import logging
from typing import List
import requests
import os
from config.constants import ORGANIZATION_NAME

# Load env variables
SALESFORCE_API_URL = os.getenv("SALESFORCE_API_URL")
SALESFORCE_ACCESS_TOKEN = os.getenv("SALESFORCE_ACCESS_TOKEN")


def sync_with_salesforce(new_sponsors: List[dict]) -> None:
    """
    Syncs new sponsor records to Salesforce API.

    Args:
        new_sponsors (List[dict]): List of enriched sponsor records.
    """
    logger = logging.getLogger("uk_sponsor_pipeline")

    if not SALESFORCE_API_URL or not SALESFORCE_ACCESS_TOKEN:
        raise ValueError("Salesforce API credentials are not properly configured.")

    if not new_sponsors:
        logger.info("✅ No new sponsors to sync with Salesforce.")
        return

    headers = {
        "Authorization": f"Bearer {SALESFORCE_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    success_count = 0
    fail_count = 0

    for sponsor in new_sponsors:
        try:
            response = requests.post(
                SALESFORCE_API_URL,
                headers=headers,
                json=sponsor
            )
            response.raise_for_status()

            # Check API-specific response content if needed
            result = response.json()
            if result.get("success") is True:
                logger.info(f"✅ Synced sponsor: {sponsor[ORGANIZATION_NAME]} ({sponsor['Route']})")
                success_count += 1
            else:
                logger.warning(f"⚠️ Salesforce responded with failure for: {sponsor[ORGANIZATION_NAME]} — {result}")
                fail_count += 1

        except requests.HTTPError as http_err:
            logger.error(f"❌ HTTP error syncing {sponsor[ORGANIZATION_NAME]}: {http_err}")
            fail_count += 1

        except Exception as err:
            logger.error(f"❌ Unexpected error syncing {sponsor[ORGANIZATION_NAME]}: {err}")
            fail_count += 1

    logger.info(f"🔄 Salesforce sync completed: {success_count} succeeded, {fail_count} failed.")

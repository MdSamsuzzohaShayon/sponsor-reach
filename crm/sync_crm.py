# crm/sync_crm.py

import logging
from typing import List
import requests
import os
from config.constants import ORGANIZATION_NAME
from crm.salesforce_api import load_token, get_salesforce_access_token

logger = logging.getLogger("uk_sponsor_pipeline")

SALESFORCE_API_URL = os.getenv("SALESFORCE_API_URL")


def sync_with_salesforce(new_sponsors: List[dict]) -> None:
    """
    Syncs new sponsor records to Salesforce API.

    Args:
        new_sponsors (List[dict]): List of enriched sponsor records.
    """
    if not SALESFORCE_API_URL:
        raise ValueError("Salesforce API URL is not properly configured.")

    if not new_sponsors:
        logger.info("✅ No new sponsors to sync with Salesforce.")
        return

    access_token = load_token()
    if not access_token:
        logger.info("🔑 No saved Salesforce token found — fetching a new one.")
        access_token = get_salesforce_access_token()

    # url = f"{SALESFORCE_API_URL}/data/v63.0/sobjects/Organization_Contracts__c/"
    url = f"{SALESFORCE_API_URL}/data/v63.0/composite/tree/Organization_Contracts__c/"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    records = []
    for index, sponsor in enumerate(new_sponsors, start=1):
        record = {
            "attributes": {
                "type": "Organization_Contracts__c",
                "referenceId": f"ref{index}"
            },
            "County__c": sponsor.get("county", "Unknown"),
            "Email__c": sponsor.get("email"),
            "Enriched__c": sponsor.get("enriched"),
            "Organization__c": sponsor.get("organization"),
            "Route__c": sponsor.get("route"),
            "Town_City__c": sponsor.get("town_city"),
            "Type_Rating__c": sponsor.get("type_rating")
        }
        records.append(record)

    payload = {"records": records}

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 401:
            logger.info("🔄 Token expired — refreshing token and retrying...")
            access_token = get_salesforce_access_token()
            headers["Authorization"] = f"Bearer {access_token}"
            response = requests.post(url, headers=headers, json=payload)

        response.raise_for_status()

        result = response.json()
        successes = [r for r in result.get("results", []) if r.get("success")]
        failures = [r for r in result.get("results", []) if not r.get("success")]

        logger.info(f"✅ Synced {len(successes)} sponsors successfully.")
        if failures:
            logger.warning(f"⚠️ {len(failures)} sponsors failed to sync: {failures}")

    except requests.HTTPError as http_err:
        logger.error(f"❌ HTTP error during bulk sync: {http_err}")
    except Exception as err:
        logger.error(f"❌ Unexpected error during bulk sync: {err}")


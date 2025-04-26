# Loops through new companies and enriches all
# enrichment/enrich_batch.py

import logging
from typing import List, Dict
from config.constants import ORGANIZATION_NAME

logger = logging.getLogger("uk_sponsor_pipeline")

def mock_enrich(company: Dict) -> Dict:
    """
    Fake enrichment for demo purposes. Replace with actual enrichment logic or API calls.
    """
    # Simulated enrichment data
    company_name = company.get(ORGANIZATION_NAME, "")
    town_city = company.get("Town/City")
    county = company.get("County")
    type_rating = company.get("Type & Rating")
    route = company.get("Route")

    enriched = {
        "organization": company_name,
        "route": route,
        "town_city": town_city,
        "county": county,
        "type_rating": type_rating,
        # "email": f"info@{company_name.lower().replace(' ', '')}.co.uk",
        "email": f"mdshayon0@gmail.com",
        "enriched": True
    }
    return enriched


def enrich_companies(companies: List[Dict]) -> List[Dict]:
    """
    Takes a list of new sponsor dictionaries and returns enriched company data.
    """
    enriched_data = []

    logger.info("🔍 Starting enrichment for new sponsors...")

    for company in companies:
        try:
            enriched = mock_enrich(company)
            enriched_data.append(enriched)
        except Exception as e:
            logger.error(f"Failed to enrich company: {company.get(ORGANIZATION_NAME, 'Unknown')} | Error: {str(e)}")

    logger.info(f"✅ Enriched {len(enriched_data)} companies successfully.")

    return enriched_data

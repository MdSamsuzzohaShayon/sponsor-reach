# Loops through new companies and enriches all
# enrichment/enrich_batch.py

import logging
from typing import List, Dict

logger = logging.getLogger("uk_sponsor_pipeline")

def mock_enrich(company: Dict) -> Dict:
    """
    Fake enrichment for demo purposes. Replace with actual enrichment logic or API calls.
    """
    # Simulated enrichment data
    company_name = company.get("Organisation Name", "")
    rown_city = company.get("Town/City")
    county = company.get("County")
    type_rating = company.get("Type & Rating")
    route = company.get("Route")

    enriched = {
        "company_name": company_name,
        "route": route,
        "rown_city": rown_city,
        "county": county,
        "type_rating": type_rating,
        "email": f"info@{company_name.lower().replace(' ', '')}.co.uk",
        "linkedIn": f"https://linkedin.com/company/{company_name.lower().replace(' ', '-')}",
        "website": f"https://{company_name.lower().replace(' ', '')}.co.uk",
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
            logger.error(f"Failed to enrich company: {company.get('Organisation Name', 'Unknown')} | Error: {str(e)}")

    logger.info(f"✅ Enriched {len(enriched_data)} companies successfully.")

    return enriched_data

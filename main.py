# Entry point – executes `daily_workflow`
# main.py
from dotenv import load_dotenv
load_dotenv()  # take environment variables

import logging
import traceback

from extraction.fetch_csv import download_latest_csv
from extraction.compare_csv import get_new_sponsors
from enrichment.enrich_batch import enrich_companies
from outreach.outreach_runner import run_outreach
from crm.sync_crm import sync_with_salesforce
from utils.logger import setup_logger
# from utils.monitor import send_alert_email
from datetime import datetime



def main():
    # Setup logger
    setup_logger()
    logger = logging.getLogger("uk_sponsor_pipeline")

    logger.info("🏁 Pipeline started...")

    try:
        # # Step 1: Download Latest CSV
        # logger.info("📥 Downloading latest UK Gov CSV...")
        # csv_path = download_latest_csv()
        #
        # # Step 2: Compare with previous CSV and detect new sponsors
        # logger.info("🔍 Comparing CSVs to find new entries...")
        # new_sponsors = get_new_sponsors(csv_path)
        #
        # if not new_sponsors:
        #     logger.info("✅ No new sponsors found today.")
        #     return
        #
        # # Step 3: Enrich sponsor data (emails, contacts, etc.)
        # logger.info(f"⚙️ Enriching {len(new_sponsors)} new sponsor(s)...")
        # enriched_data = enrich_companies(new_sponsors)

        # Step 4: Send Outreach Emails
        # logger.info("📧 Sending outreach emails...")
        # run_outreach(enriched_data)

        enriched_data = [{'company_name': 'A & N TRIMMINGS LIMITED', 'county': "nan", 'email': 'info@a&ntrimmingslimited.co.uk', 'enriched': True, 'linkedIn': 'https://linkedin.com/company/a-&-n-trimmings-limited', 'route': 'Skilled Worker', 'rown_city': 'SOLIHULL', 'type_rating': 'Worker (A rating)', 'website': 'https://a&ntrimmingslimited.co.uk'},]

        # Step 5: Sync with Salesforce CRM
        logger.info("🔄 Syncing with Salesforce CRM...")
        sync_with_salesforce(enriched_data)

        logger.info("✅ Pipeline completed successfully!")

    except Exception as e:
        error_msg = f"❌ Pipeline failed: {str(e)}\n\n{traceback.format_exc()}"
        logger.error(error_msg)

        # Optional: Alert via email/Slack
        # send_alert_email("UK Sponsor Pipeline Failed", error_msg)

if __name__ == "__main__":
    main()

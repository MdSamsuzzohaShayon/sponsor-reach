# Main runner: extraction → enrichment → email → CRM
"""
Main workflow runner for the UK Sponsor Reach pipeline.
Executes in order:
1. Download latest UK sponsor CSV
2. Compare with previous data to detect new sponsors
3. Enrich new sponsors using third-party APIs
4. Send outreach emails to new sponsors
5. Sync enriched data to Salesforce CRM
"""

import logging
from datetime import datetime
from pathlib import Path

from utils.logger import setup_logger
from utils.monitor import send_alert
from extraction.fetch_csv import download_latest_csv
from extraction.compare_csv import detect_new_sponsors
from extraction.parse_sponsors import preprocess_sponsor_data
from enrichment.enrich_batch import enrich_companies
from outreach.outreach_runner import run_outreach
from crm.sync_crm import sync_with_salesforce

# Initialize logging
setup_logger()
logger = logging.getLogger(__name__)


def daily_pipeline() -> bool:
    """
    Execute the full sponsor pipeline workflow.
    Returns True if successful, False if any stage fails.
    """
    try:
        logger.info("🚀 Starting UK Sponsor Reach daily pipeline")
        start_time = datetime.now()

        # 1. Download latest sponsor data
        logger.info("⬇️ Downloading latest sponsor CSV from UK Gov")
        raw_csv_path = download_latest_csv()
        if not raw_csv_path or not Path(raw_csv_path).exists():
            raise FileNotFoundError("Failed to download sponsor CSV")

        # 2. Preprocess and compare with previous data
        logger.info("🔍 Comparing with previous sponsor data")
        df_sponsors = preprocess_sponsor_data(raw_csv_path)
        new_sponsors = detect_new_sponsors(df_sponsors)

        if new_sponsors.empty:
            logger.info("🔄 No new sponsors found - ending pipeline")
            return True

        logger.info(f"🎯 Found {len(new_sponsors)} new sponsors to process")

        # 3. Enrich new sponsor data
        logger.info("✨ Enriching new sponsor data via APIs")
        enriched_sponsors = enrich_companies(new_sponsors)

        # 4. Send outreach emails
        logger.info("📧 Launching outreach campaign")
        email_stats = run_outreach(enriched_sponsors)
        logger.info(f"✉️ Email results: {email_stats.get('success', 0)} sent, {email_stats.get('failed', 0)} failed")

        # 5. Sync with Salesforce
        logger.info("🔄 Syncing enriched data with Salesforce")
        crm_results = sync_with_salesforce(enriched_sponsors)
        logger.info(
            f"✅ CRM sync complete: {crm_results.get('created', 0)} created, {crm_results.get('updated', 0)} updated")

        # Pipeline completed successfully
        duration = (datetime.now() - start_time).total_seconds() / 60
        logger.info(f"🏁 Pipeline completed successfully in {duration:.2f} minutes")
        return True

    except Exception as e:
        logger.critical(f"❌ Pipeline failed: {str(e)}", exc_info=True)
        send_alert(
            subject="UK Sponsor Pipeline Failure",
            message=f"Error during daily workflow: {str(e)}",
            priority="high"
        )
        return False


if __name__ == "__main__":
    success = daily_pipeline()
    if not success:
        exit(1)  # Exit with error code for cron monitoring
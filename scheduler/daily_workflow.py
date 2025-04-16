# scheduler/daily_workflow.py

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
from extraction.compare_csv import get_new_sponsors
from extraction.parse_sponsors import preprocess_sponsor_data
from enrichment.enrich_batch import enrich_companies
from outreach.outreach_runner import run_outreach
from crm.sync_crm import sync_with_salesforce


def daily_pipeline() -> bool:
    """Execute the full sponsor pipeline workflow."""
    setup_logger()
    logger = logging.getLogger("uk_sponsor_pipeline")

    logger.info("🚀 Starting UK Sponsor Reach daily pipeline")
    start_time = datetime.now()

    try:
        # 1. Download latest sponsor data
        logger.info("⬇️ Downloading latest sponsor CSV")
        raw_csv_path = download_latest_csv()
        if not raw_csv_path or not Path(raw_csv_path).exists():
            raise FileNotFoundError("❌ Sponsor CSV not downloaded or missing")

        # 2. Preprocess and compare with previous data
        logger.info("🔍 Preprocessing and comparing with previous data")
        df_sponsors = preprocess_sponsor_data(raw_csv_path)
        new_sponsors = get_new_sponsors(df_sponsors)

        if len(new_sponsors) == 0:
            logger.info("🔄 No new sponsors found — ending pipeline")
            return True

        logger.info(f"🎯 Found {len(new_sponsors)} new sponsors")

        # 3. Enrich new sponsors
        logger.info("✨ Enriching new sponsor data")
        enriched_sponsors = enrich_companies(new_sponsors)

        if len(enriched_sponsors) == 0:
            logger.warning("⚠️ No enrichment data received, proceeding without outreach and CRM sync")
            return False

        # 4. Send outreach emails
        logger.info("📧 Sending outreach emails")
        # email_stats = run_outreach(enriched_sponsors)
        # logger.info(f"✉️ Email results: {email_stats.get('success', 0)} sent, {email_stats.get('failed', 0)} failed")

        # 5. Sync with Salesforce
        logger.info("🔄 Syncing with Salesforce")
        sync_with_salesforce(enriched_sponsors)

        duration = (datetime.now() - start_time).total_seconds() / 60
        logger.info(f"🏁 Pipeline completed in {duration:.2f} minutes")

        return True

    except FileNotFoundError as fnf_error:
        logger.error(f"❌ File error: {fnf_error}", exc_info=True)
        send_alert(f"UK Sponsor Pipeline Failure: {fnf_error}")
        return False

    except Exception as e:
        logger.critical(f"❌ Unexpected error: {e}", exc_info=True)
        send_alert(
            subject="UK Sponsor Pipeline Failure",
            message=f"Critical failure during daily workflow: {str(e)}",
            priority="high"
        )
        return False

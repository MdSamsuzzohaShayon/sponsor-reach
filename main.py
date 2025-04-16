# main.py

"""
Main entry point for the UK Sponsor Reach pipeline.
Initializes logging, handles errors, and executes the daily workflow.
"""
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

import logging
from utils.logger import setup_logger
from utils.monitor import send_alert
from scheduler.daily_workflow import daily_pipeline


def main():
    """Main execution function."""


    setup_logger()
    logger = logging.getLogger("main")

    logger.info("🚀 Starting UK Sponsor Reach pipeline")

    try:
        success = daily_pipeline()

        if success:
            logger.info("✅ Pipeline completed successfully")
        else:
            logger.error("❌ Pipeline failed — see logs for details")
            send_alert("Error", "UK Sponsor Reach Pipeline failed. Check logs.")
            exit(1)

    except Exception as e:
        logger.critical(f"💥 Fatal error occurred: {e}", exc_info=True)
        send_alert("Error",f"Pipeline Failure: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()

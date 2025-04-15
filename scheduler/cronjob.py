# cronjob.py
"""
Cron job wrapper for the UK Sponsor Reach pipeline.
Manages:
- Lock file to prevent overlapping runs
- Dependency verification
- Logging
- Error escalation
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

# Set up paths
PROJECT_ROOT = Path(__file__).parent.resolve()
LOCK_FILE = PROJECT_ROOT / "data/locks/pipeline.lock"
LOG_FILE = PROJECT_ROOT / "data/logs/cron.log"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('cron_scheduler')

def check_dependencies() -> bool:
    """Verify critical Python dependencies."""
    try:
        import pandas
        import requests
        from simple_salesforce import Salesforce
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {str(e)}")
        return False

def create_lock() -> bool:
    """Create a lock file to prevent concurrent runs."""
    try:
        LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        return True
    except Exception as e:
        logger.error(f"Failed to create lock file: {str(e)}")
        return False

def release_lock() -> bool:
    """Remove the lock file."""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
        return True
    except Exception as e:
        logger.error(f"Failed to remove lock file: {str(e)}")
        return False

def is_already_running() -> bool:
    """Check if another pipeline instance is running."""
    if not LOCK_FILE.exists():
        return False

    try:
        with open(LOCK_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return True
    except (OSError, ValueError):
        return False

def main():
    logger.info("⏰ Starting UK Sponsor Reach cron job")
    start_time = datetime.now()

    if is_already_running():
        logger.error("🚨 Pipeline already running - aborting")
        sys.exit(1)

    if not check_dependencies():
        logger.error("❌ Missing dependencies - aborting")
        sys.exit(1)

    if not create_lock():
        sys.exit(1)

    try:
        from scheduler.daily_workflow import daily_pipeline

        logger.info("🔄 Running daily workflow...")
        success = daily_pipeline()

        if not success:
            logger.error("❌ Pipeline failed")
            sys.exit(1)

    except Exception as e:
        logger.critical(f"💥 Unexpected error: {str(e)}", exc_info=True)
        sys.exit(1)
    finally:
        release_lock()

    duration = (datetime.now() - start_time).total_seconds() / 60
    logger.info(f"✅ Cron job completed in {duration:.2f} minutes")

if __name__ == "__main__":
    main()

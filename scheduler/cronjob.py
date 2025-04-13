# Shell script to run via cron / task scheduler

import os
import sys
import logging
from pathlib import Path
from datetime import datetime

"""
Cron job scheduler for UK Sponsor Reach pipeline.
Handles:
- Lock files to prevent overlapping runs
- Proper logging redirection
- Error notification escalation
- Dependency verification
"""


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
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('cron_scheduler')


def check_dependencies():
    """Verify all required dependencies are available"""
    try:
        import pandas
        import requests
        from simple_salesforce import Salesforce
        # Add other critical imports
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {str(e)}")
        return False


def create_lock():
    """Create lock file to prevent overlapping runs"""
    try:
        LOCK_FILE.parent.mkdir(exist_ok=True)
        with open(LOCK_FILE, 'w') as f:
            f.write(str(os.getpid()))
        return True
    except Exception as e:
        logger.error(f"Failed to create lock file: {str(e)}")
        return False


def release_lock():
    """Remove the lock file"""
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
        return True
    except Exception as e:
        logger.error(f"Failed to remove lock file: {str(e)}")
        return False


def is_already_running():
    """Check if another instance is running"""
    if not LOCK_FILE.exists():
        return False

    try:
        with open(LOCK_FILE, 'r') as f:
            pid = int(f.read().strip())

        # Check if process still exists
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    except Exception:
        return False


def main():
    logger.info("⏰ Starting UK Sponsor Reach cron job")
    start_time = datetime.now()

    # Check for existing runs
    if is_already_running():
        logger.error("🚨 Pipeline is already running - aborting")
        sys.exit(1)

    # Verify dependencies
    if not check_dependencies():
        logger.error("❌ Missing required dependencies")
        sys.exit(1)

    # Create lock file
    if not create_lock():
        sys.exit(1)

    try:
        # Run the main pipeline
        from scheduler.daily_workflow import daily_pipeline

        logger.info("🔄 Executing daily workflow...")
        success = daily_pipeline()

        if not success:
            logger.error("❌ Pipeline failed - check logs for details")
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
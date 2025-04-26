# Sends alerts via email/Slack on failure
# utils/monitor.py

import logging
import os
from outreach.send_email import send_email

# Set up logger
logger = logging.getLogger("monitor")


def send_alert(subject: str, message: str = None, priority: str = "normal"):
    """Send alert via email with details about failures or critical errors."""
    alert_email = os.getenv("ALERT_EMAIL")  # Recipient email from .env file
    if not alert_email:
        logger.warning("ALERT_EMAIL not found in environment variables!")
        return

    # Default to a generic message if none provided
    message = message or "An alert was triggered, but no additional details were provided."

    try:
        send_email(to=alert_email, subject=subject, html=message)
        logger.info(f"Alert sent to {alert_email}: {subject}")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")


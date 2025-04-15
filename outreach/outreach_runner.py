# Picks enriched contacts and launches email
# outreach/outreach_runner.py

import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from .send_email import send_email  # Assumes you have a send_email function
from typing import List, Dict

# Set up logger
logger = logging.getLogger("uk_sponsor_pipeline")

# Setup Jinja2 environment for templates
env = Environment(
    loader=FileSystemLoader("outreach/email_templates"),
    autoescape=select_autoescape(["html", "xml"])
)

def run_outreach(enriched_data: List[Dict]):
    """
    Loops through enriched sponsor data and sends personalized emails.
    """
    template = env.get_template("outreach_template.html")

    # success_count = 0
    # failure_count = 0
    #
    # for sponsor in enriched_data:
    #     try:
    #         email = sponsor.get("email")
    #         name = sponsor.get("route", "there")
    #         company = sponsor.get("company_name", "your organization")
    #
    #         if not email:
    #             logger.warning(f"Skipping sponsor with no email: {sponsor}")
    #             continue
    #
    #         # Render personalized email content
    #         subject = f"UK Sponsor Licence Opportunity – {company}"
    #         html_content = template.render(contact_name=name, company_name=company)
    #
    #         # Send the email
    #         send_email(to=email, subject=subject, html=html_content)
    #
    #         logger.info(f"📨 Email sent to {email}")
    #         success_count += 1
    #
    #     except Exception as e:
    #         logger.error(f"❌ Failed to send email to {sponsor.get('email')}: {str(e)}")
    #         failure_count += 1
    # logger.info(f"✅ Outreach Summary: {success_count} sent, {failure_count} failed.")

    emails = [sponsor.get("email") for sponsor in enriched_data if sponsor.get("email")]
    if not emails:
        logger.warning("No valid emails found to send.")
        return

        # Prepare subject and content (can be generic or list the sponsors)
    subject = "UK Sponsor Licence Opportunity"
    html_content = template.render(contact_name="Sponsor", company_name="your organization")

    try:
        # Send one email to all
        send_email(to=emails, subject=subject, html=html_content)
        logger.info(f"📨 Email sent to {len(emails)} sponsors: {emails}")

    except Exception as e:
        logger.error(f"❌ Failed to send bulk email: {str(e)}")



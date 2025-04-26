import os
import boto3
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.exceptions import ClientError
from typing import List, Optional, Union

# Set up logger
logger = logging.getLogger("send_email")

def send_email(
    to: Union[str, List[str]],
    subject: str,
    html: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
):
    """Tries sending email using SES first, then SMTP as fallback"""
    try:
        # send_email_ses(to, subject, html, cc, bcc)
        send_email_native(to, subject, html, cc, bcc)
    except Exception as e:
        logger.error(f"Failed to send email via SES: {e}, falling back to SMTP.")
        # send_email_native(to, subject, html, cc, bcc)


def send_email_ses(
    to: Union[str, List[str]],
    subject: str,
    html: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
):
    """Send email using Amazon SES"""
    ses_client = boto3.client(
        'ses',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    if isinstance(to, str):
        to = [to]
    cc = cc or []
    bcc = bcc or []

    try:
        response = ses_client.send_email(
            Source=os.getenv("SES_FROM_EMAIL"),
            Destination={
                'ToAddresses': to,
                'CcAddresses': cc,
                'BccAddresses': bcc
            },
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Html': {'Data': html, 'Charset': 'UTF-8'}
                }
            }
        )
        logger.info(f"✅ Email sent via SES to: {to + cc + bcc}")
        return response
    except ClientError as e:
        logger.error(f"SES ClientError: {e}")
        raise Exception(f"SES email sending failed: {e}")


def send_email_native(
    to: Union[str, List[str]],
    subject: str,
    html: str,
    cc: Optional[List[str]] = None,
    bcc: Optional[List[str]] = None
):
    """Send email using native smtplib (SMTP)"""
    from_email = os.getenv("SMTP_FROM_EMAIL")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if isinstance(to, str):
        to = [to]
    cc = cc or []
    bcc = bcc or []

    all_recipients = to + cc + bcc

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = ", ".join(to)
    if cc:
        message["Cc"] = ", ".join(cc)

    html_part = MIMEText(html, "html")
    message.attach(html_part)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, all_recipients, message.as_string())
        logger.info(f"✅ Email sent via SMTP to: {all_recipients}")
        return {"Message": "Email sent successfully via SMTP."}
    except Exception as e:
        logger.error(f"SMTP Exception: {e}")
        raise Exception(f"SMTP email sending failed: {e}")

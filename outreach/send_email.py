# outreach/send_email.py
import os
import boto3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from botocore.exceptions import ClientError

# https://aws.amazon.com/ses/pricing/
# https://docs.aws.amazon.com/ses/latest/dg/setting-up.html?sc_ichannel=ha&sc_icampaign=acq_awsblogsb&sc_icontent=messaging-resources
# https://docs.aws.amazon.com/ses/latest/dg/send-email-raw.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ses-template.html
def send_email(to: str, subject: str, html: str):
    # send_email_ses(to, subject, html)
    send_email_native(to, subject, html)





def send_email_ses(to: str, subject: str, html: str):
    """Send email using Amazon SES"""
    ses_client = boto3.client(
        'ses',
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    try:
        response = ses_client.send_email(
            Source='your_email@example.com',  # Must be verified in SES
            Destination={'ToAddresses': [to]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Html': {'Data': html, 'Charset': 'UTF-8'}
                }
            }
        )
        return response
    except ClientError as e:
        return e.response['Error']


def send_email_native(to: str, subject: str, html: str):
    """Send email using built-in smtplib"""
    from_email = os.getenv("SMTP_FROM_EMAIL")
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = from_email
    message["To"] = to

    html_part = MIMEText(html, "html")
    message.attach(html_part)

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            server.sendmail(from_email, to, message.as_string())
        return {"Message": "Email sent successfully via Python SMTP."}
    except Exception as e:
        return {"Error": str(e)}




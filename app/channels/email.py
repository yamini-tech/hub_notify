"""
Email channel — sends via SMTP (dev) or AWS SES (prod).

Updated: Includes Jinja2 template support and production-ready structure.
"""
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings

# Setup Jinja2 environment for HTML templates
# Assumes templates are stored in a 'templates' folder at project root
template_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

async def send_email(
    to: str,
    subject: str,
    body: str,
    template_name: str | None = None,
    template_context: dict | None = None,
) -> str:
    """
    Send an email via SMTP (local) or AWS SES (production).

    Returns the SMTP message ID on success.
    Raises an exception on failure.
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = settings.smtp_from_email
    msg["To"] = to
    msg["Subject"] = subject
    
    # Always attach the plain text body
    msg.attach(MIMEText(body, "plain"))

    # If a template is provided, render and attach the HTML
    if template_name:
        template = template_env.get_template(template_name)
        html_content = template.render(template_context or {})
        msg.attach(MIMEText(html_content, "html"))

    # Send via SMTP/SES
    # NOTE: Ensure settings.smtp_host, username, and password are 
    # configured for AWS SES endpoint in production.
    await aiosmtplib.send(
        msg,
        hostname=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=settings.smtp_use_tls, # Ensure this is True for SES
        start_tls=settings.smtp_start_tls,
    )
    
    return msg["Message-ID"] or "sent"
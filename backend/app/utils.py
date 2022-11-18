"""Shared utilities"""

import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, Optional

import emails
from emails.template import JinjaTemplate
from jose import jwt

from app.core.config import SETTINGS

LOGGER = logging.getLogger(__name__)


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = None,
):
    """
    Send an email

    :param email_to: Destination email address
    :param subject_template: Template of the subject
    :param html_template: Template of the email body, in HTML
    :param environment: Dictionary of variables to use in tempaltes
    """
    assert SETTINGS.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(SETTINGS.EMAILS_FROM_NAME, SETTINGS.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": SETTINGS.SMTP_HOST, "port": SETTINGS.SMTP_PORT}
    if SETTINGS.SMTP_TLS:
        smtp_options["tls"] = True
    if SETTINGS.SMTP_USER:
        smtp_options["user"] = SETTINGS.SMTP_USER
    if SETTINGS.SMTP_PASSWORD:
        smtp_options["password"] = SETTINGS.SMTP_PASSWORD
    if environment is None:
        environment = {}
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    LOGGER.info("Sent email to %s. Response: %s", email_to, response)


def send_test_email(email_to: str):
    """
    Send a test email

    :param email_to: Destination email address
    """
    project_name = SETTINGS.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(SETTINGS.EMAIL_TEMPLATES_DIR) / "test_email.html", "r", encoding="utf8") as fis:
        template_str = fis.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": SETTINGS.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str):
    """
    Send an email dedicated to reset a user's password

    :param email_to: Destination email address
    :param email: Email of the user to reset the password
    :param token: Reset-token password
    """
    project_name = SETTINGS.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(
        Path(SETTINGS.EMAIL_TEMPLATES_DIR) / "reset_password.html", "r", encoding="utf8"
    ) as fis:
        template_str = fis.read()
    server_host = SETTINGS.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": SETTINGS.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": SETTINGS.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    """
    Generate a token to reset a user's password

    :param email: User's email
    :return: Reset-password token
    """
    delta = timedelta(hours=SETTINGS.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        SETTINGS.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Check an decode a reset-password token

    :param token: Token to decode
    :return: Decoded token or None if token unable to be decoded
    """
    try:
        decoded_token = jwt.decode(token, SETTINGS.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None

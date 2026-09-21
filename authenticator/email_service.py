import logging
import os
from typing import Any, Dict, List, Optional
import requests

logger = logging.getLogger(__name__)

SENDLIB_URL = "https://sendlib.samueltuoyo.com/api/send"


def send_email_via_sendlib(
    to: str,
    subject: str,
    html: str,
    from_email: Optional[str] = None,
    text: Optional[str] = None,
    reply_to: Optional[str] = None,
    attachments: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Send an email using the Sendlib API."""
    api_key = os.getenv("SENDLIB_KEY")
    if not api_key:
        raise ValueError("SENDLIB_KEY environment variable is not configured.")

    sender = from_email or os.getenv("DEFAULT_FROM_EMAIL", "yourproduct@gmail.com")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload: Dict[str, Any] = {
        "from": sender,
        "to": to,
        "subject": subject,
        "html": html,
    }

    if text:
        payload["text"] = text
    if reply_to:
        payload["replyTo"] = reply_to
    if attachments:
        payload["attachments"] = attachments

    response = requests.post(SENDLIB_URL, json=payload, headers=headers, timeout=10)
    data = response.json() if response.content else {}

    if not response.ok:
        logger.error(f"Sendlib error [{response.status_code}]: {data}")
        raise RuntimeError(data.get("message") or f"Sendlib request failed with status {response.status_code}")

    return data

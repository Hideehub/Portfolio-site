import logging
import time

from django.conf import settings
from django.core.cache import cache
from django.core.mail import EmailMessage, mailers

logger = logging.getLogger(__name__)

def client_ip(request):
    # Render sits behind a proxy, so the client IP is the first X-Forwarded-For entry.
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def is_rate_limited(request):
    """Count this submission and return True if the IP is over the limit.

    Uses a fixed window per IP so the count expires cleanly with any cache backend.
    """
    window = settings.CONTACT_RATE_WINDOW
    bucket = int(time.time() // window)
    key = f"contact-rate:{client_ip(request)}:{bucket}"
    count = cache.get(key, 0) + 1
    cache.set(key, count, timeout=window)
    return count > settings.CONTACT_RATE_LIMIT


def email_configured():
    return bool(settings.CONTACT_RECIPIENT_EMAIL) and "default" in mailers


def send_notification(message):
    """Email the site owner about a new message. Never raises."""
    if not email_configured():
        return False
    email = EmailMessage(
        subject=f"Portfolio contact from {message.name}",
        body=f"From: {message.name} <{message.email}>\n\n{message.message}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_RECIPIENT_EMAIL],
        reply_to=[message.email],
    )
    try:
        email.send(using="default")
    except Exception:
        logger.exception("Failed to send contact notification for message %s", message.pk)
        return False
    return True

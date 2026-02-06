import logging
from django.dispatch import receiver
from django.contrib.auth.signals import user_login_failed

logger = logging.getLogger('django.security')


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    ip = "UNKNOWN"

    if request is not None:
        ip = request.META.get('REMOTE_ADDR', 'UNKNOWN')

    logger.warning(
        "FAILED LOGIN | user=%s | ip=%s",
        credentials.get('username'),
        ip
    )


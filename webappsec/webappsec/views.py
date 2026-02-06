import logging
from django.shortcuts import render

logger = logging.getLogger('django.security')


def custom_403_view(request, exception=None):
    user = request.user if request.user.is_authenticated else "ANONYMOUS"

    logger.warning(
        "UNAUTHORIZED ACCESS (403) | user=%s | path=%s | ip=%s",
        user,
        request.path,
        request.META.get('REMOTE_ADDR')
    )

    return render(request, "403.html", status=403)


def custom_404_view(request, exception=None):
    user = request.user if request.user.is_authenticated else "ANONYMOUS"

    logger.warning(
        "RESOURCE NOT FOUND (404) | user=%s | path=%s | ip=%s",
        user,
        request.path,
        request.META.get('REMOTE_ADDR')
    )

    return render(request, "404.html", status=404)

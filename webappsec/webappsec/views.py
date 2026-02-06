import logging
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

logger = logging.getLogger('django.security')


def custom_403_view(request, exception=None):
    user = request.user.username if request.user.is_authenticated else "ANONYMOUS"

    logger.warning(
        "UNAUTHORIZED ACCESS (403) | user=%s | path=%s | ip=%s",
        user,
        request.path,
        request.META.get('REMOTE_ADDR', 'UNKNOWN')
    )

    return render(request, "403.html", status=403)


def custom_404_view(request, exception=None):
    user = request.user.username if request.user.is_authenticated else "ANONYMOUS"

    logger.warning(
        "RESOURCE NOT FOUND (404) | user=%s | path=%s | ip=%s",
        user,
        request.path,
        request.META.get('REMOTE_ADDR', 'UNKNOWN')
    )

    return render(request, "404.html", status=404)


@method_decorator(
    ratelimit(key='ip', rate='5/m', block=False),  # ❗ block=False
    name='dispatch'
)
class RateLimitedLoginView(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        # 🔐 RATE LIMIT TRIGGERED
        if getattr(request, 'limited', False):
            logger.warning(
                "RATE LIMIT TRIGGERED (429) | user=%s | path=%s | ip=%s",
                request.POST.get('username', 'UNKNOWN'),
                request.path,
                request.META.get('REMOTE_ADDR', 'UNKNOWN')
            )
            return render(request, "429.html", status=429)

        return super().dispatch(request, *args, **kwargs)

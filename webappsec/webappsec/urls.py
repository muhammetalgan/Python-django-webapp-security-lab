from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from webappsec.views import RateLimitedLoginView
urlpatterns = [
    # Django admin (default security model)
    path('admin/', admin.site.urls),

    # Auth
    path('login/', RateLimitedLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # App
    path('', include('tasks.urls')),
]

# Custom error handlers
handler403 = 'webappsec.views.custom_403_view'
handler404 = 'webappsec.views.custom_404_view'

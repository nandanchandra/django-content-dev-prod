from django.conf import settings
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("djoser.urls.jwt")),
    path("api/v1/account/", include("api.account.urls")),
]

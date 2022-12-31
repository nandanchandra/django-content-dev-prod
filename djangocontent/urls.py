from django.conf import settings
from django.contrib import admin
from django.urls import path,include

from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="DjangoContent",
        default_version="v1",
        description="API endpoints for the DjangoContent API",
        contact=openapi.Contact(email="chandranandan.chandrakar@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("redocument/",schema_view.with_ui(cache_timeout=0)),
    path("api/v1/account/", include("api.account.urls")),
    path("api/v1/post/", include("api.post.urls")),
    path("api/v1/services/", include("api.services.urls")),
]

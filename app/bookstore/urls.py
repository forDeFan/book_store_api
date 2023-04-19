"""Central file for url mappings/ menaging."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import debug
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include endpoints from user api
    path("api/user/", include("user.urls")),
    # Include endpoints from book api
    path("api/book/", include("book.urls")),
    # API docs endpoints
    path(
        "api/schema/", SpectacularAPIView.as_view(), name="api-schema"
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Images

"""Central file for url mappings/ menaging."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import debug

urlpatterns = [
    # Default django site - just to see something at app start.
    path("", debug.default_urlconf),
    path("admin/", admin.site.urls),
    # Include endpoints from user api
    path("api/user/", include("user.urls")),
    # Include endpoints from book api
    path("api/book/", include("book.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Images

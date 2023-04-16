"""Central file for url mappings/ menaging."""

from django.contrib import admin
from django.urls import include, path


from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include endpoints from user api
    path("api/user/", include("user.urls")),
    # Include endpoints from book api
    path("api/book/", include("book.urls")),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # Images

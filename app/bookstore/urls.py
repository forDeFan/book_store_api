"""Central file for url mappings/ menaging."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include endpoints from user api
    path("api/user/", include("user.urls")),
    # Include endpoints from book api
    path("api/book/", include("book.urls")),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # Include endpoint from user app
    path("api/user/", include("user.urls")),
]

"""User API endpoints defined here."""

from django.urls import path
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "user"

urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="refresh"), # Extend session time endpoint.
    path("logout/", views.LogoutView.as_view(), name="logout"),
]

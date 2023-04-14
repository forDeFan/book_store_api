"""User API endpoints defined here."""

from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    path("register/", views.CreateUser.as_view(), name="register")
]

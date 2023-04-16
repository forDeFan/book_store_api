"""Book API endpoints defined here."""

from book import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from core.models import Book
from django_filters.views import FilterView

# Uses API viewe to automatically create routes for options
# avalilable in that view
router = DefaultRouter()
router.register("", views.BookViewSet)

app_name = "Book"

urlpatterns = [
    path("", include(router.urls)), 
    path("list/", FilterView.as_view(model=Book), name="book-list"),]

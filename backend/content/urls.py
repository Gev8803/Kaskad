from django.urls import path

from .views import ContactCreateView, ContentView

urlpatterns = [
    path("content/", ContentView.as_view(), name="api-content"),
    path("contact/", ContactCreateView.as_view(), name="api-contact"),
]

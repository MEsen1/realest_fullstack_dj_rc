from django.urls import path, include
from .views import ContactCreateView

urlpatterns = [path("", ContactCreateView.as_view())]

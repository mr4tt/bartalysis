from django.urls import path
from .views import get_departures

urlpatterns = [
    path('departures/', get_departures),
]
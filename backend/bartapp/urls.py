from django.urls import path
from rest_framework.router import DefaultRouter
from .views import get_departures
from .views import get_agencies
from .views import RouteViewSet, StopViewSet, TripViewSet, StopTimeViewSet, AgencyViewSet, CalendarViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet)
router.register(r'stops', StopViewSet)
router.register(r'trips', TripViewSet)
router.register(r'stop_times', StopTimeViewSet)
router.register(r'agencies', AgencyViewSet)
router.register(r'calendar', CalendarViewSet)

urlpatterns = [
    path('api/departures/', get_departures, name = 'departures'),
    path('agencies/', get_agencies, name = 'agencies'),
    path('', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    get_departures,
    get_agencies,
    AgencyViewSet,
    RouteViewSet,
    StopViewSet,
    TripViewSet,
    StopTimeViewSet,
    CalendarViewSet,
    FeedInfoViewSet,
    # FareAttributeViewSet,
    # FareRuleViewSet,
    # RiderCategoryViewSet,
    # FareRiderCategoryViewSet,
    # ShapeViewSet,
    # RouteAttributeViewSet,
    # RealtimeRouteViewSet,
    # DirectionViewSet,
    # TransferViewSet,
    # CalendarAttributeViewSet,
    # CalendarDateViewSet,
    # RtStopTimeUpdateViewSet,
    # RtAlertViewSet,
    # RtTripViewSet,
    IncomingTrainsView
)

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'stops', StopViewSet, basename='stop')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'stop_times', StopTimeViewSet, basename='stoptime')
router.register(r'calendar', CalendarViewSet, basename='calendar')
router.register(r'feed_info', FeedInfoViewSet, basename='feedinfo')
# router.register(r'fare_attributes', FareAttributeViewSet, basename='fareattribute')
# router.register(r'fare_rules', FareRuleViewSet, basename='farerule')
# router.register(r'rider_categories', RiderCategoryViewSet, basename='ridercategory')
# router.register(r'fare_rider_categories', FareRiderCategoryViewSet, basename='fareridercategory')
# router.register(r'shapes', ShapeViewSet, basename='shape')
# router.register(r'route_attributes', RouteAttributeViewSet, basename='routeattribute')
# router.register(r'realtime_routes', RealtimeRouteViewSet, basename='realtimeroute')
# router.register(r'directions', DirectionViewSet, basename='direction')
# router.register(r'transfers', TransferViewSet, basename='transfer')
# router.register(r'calendar_attributes', CalendarAttributeViewSet, basename='calendarattribute')
# router.register(r'calendar_dates', CalendarDateViewSet, basename='calendardate')
# router.register(r'rt_stop_time_updates', RtStopTimeUpdateViewSet, basename='rtstoptimeupdate')
# router.register(r'rt_alerts', RtAlertViewSet, basename='rtalert')
# router.register(r'rt_trips', RtTripViewSet, basename='rttrip')

urlpatterns = [
    path('api/departures/', get_departures, name='departures'),
    path('api/agencies/', get_agencies, name='agencies'),
    path('api/', include(router.urls)),
    path('api/incoming_trains/<int:station_id>/', IncomingTrainsView.as_view(), name='incoming_trains'),
]

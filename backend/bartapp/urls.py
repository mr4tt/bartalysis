from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    home,
    get_departures,
    get_agencies,
    AgencyViewSet,
    RouteViewSet,
    StopViewSet,
    TripViewSet,
    StopTimeViewSet,
    CalendarViewSet,
    FeedInfoViewSet,
    FareAttributeViewSet,
    FareRuleViewSet,
    RiderCategoryViewSet,
    FareRiderCategoryViewSet,
    ShapeViewSet,
    RouteAttributeViewSet,
    RealtimeRouteViewSet,
    DirectionViewSet,
    TransferViewSet,
    CalendarAttributeViewSet,
    CalendarDateViewSet,
    RealtimeStopTimeUpdateViewSet,
    RealtimeAlertViewSet,
    RealtimeTripViewSet,

    # RoutePlannerView,
    # RoutePlannerView2,
    AlertInfoView,
    FareView,
    StopTimeUpdateView,
    LateTripsView,
    ActiveTrainsView,
    # PlanRouteView,
    StationInfoView,
    StationScheduleView,
    StationAccessView,
    ScheduleInfoArriveView,
    ScheduleInfoDepartView,
)

router = DefaultRouter()
router.register(r'agencies', AgencyViewSet, basename='agency')
router.register(r'routes', RouteViewSet, basename='route')
router.register(r'stops', StopViewSet, basename='stop')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'stop_times', StopTimeViewSet, basename='stoptime')
router.register(r'calendar', CalendarViewSet, basename='calendar')
router.register(r'feed_info', FeedInfoViewSet, basename='feedinfo')
router.register(r'fare_attributes', FareAttributeViewSet, basename='fareattribute')
router.register(r'fare_rules', FareRuleViewSet, basename='farerule')
router.register(r'rider_categories', RiderCategoryViewSet, basename='ridercategory')
router.register(r'fare_rider_categories', FareRiderCategoryViewSet, basename='fareridercategory')
router.register(r'shapes', ShapeViewSet, basename='shape')
router.register(r'route_attributes', RouteAttributeViewSet, basename='routeattribute')
router.register(r'realtime_routes', RealtimeRouteViewSet, basename='realtimeroute')
router.register(r'directions', DirectionViewSet, basename='direction')
router.register(r'transfers', TransferViewSet, basename='transfer')
router.register(r'calendar_attributes', CalendarAttributeViewSet, basename='calendarattribute')
router.register(r'calendar_dates', CalendarDateViewSet, basename='calendardate')
router.register(r'realtime_stop_time_updates', RealtimeStopTimeUpdateViewSet, basename='realtimestoptimeupdate')
router.register(r'realtime_alerts', RealtimeAlertViewSet, basename='realtimealert')
router.register(r'realtime_trips', RealtimeTripViewSet, basename='realtimetrip')


urlpatterns = [
    path('', home, name='home'), # Home page
    path('router/', include(router.urls)), # API routes
    path('api/departures/', get_departures, name='departures'), # For testing purposes only. Returns JSON data from BART API.
    # path('route-planner/<str:start_station>/<str:end_station>/', RoutePlannerView.as_view(), name='route_planner'),
    # path('route-planner2/<str:start_station>/<str:end_station>/', RoutePlannerView2.as_view(), name='route_planner2'),

    path('api/alerts/', AlertInfoView.as_view(), name='alerts'),
    path('api/fare', FareView.as_view(), name='fare'),
    path('api/stop_time_updates/<str:stop_id>/', StopTimeUpdateView.as_view(), name='stop_time_updates'),
    path('api/late-trips/', LateTripsView.as_view(), name='late-trips'),
    path('api/active-trains/', ActiveTrainsView.as_view(), name='active-trains'),
    # path('plan_route/<str:start_station>/<str:end_station>/', PlanRouteView.as_view(), name='plan_route'),
    path('api/station-info/', StationInfoView.as_view(), name='station-info'),
    path('api/station-schedule/', StationScheduleView.as_view(), name='station-schedule'),
    path('api/station-access/', StationAccessView.as_view(), name='station-access'),
    path('api/schedule-info-arrive/', ScheduleInfoArriveView.as_view(), name='schedule-info-arrive'),
    path('api/schedule-info-depart/', ScheduleInfoDepartView.as_view(), name='schedule-info-depart'),

]
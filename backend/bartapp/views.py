import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection, connections
from django.utils import timezone
from django.db.models import F, OuterRef, Subquery, Count

from rest_framework import serializers, status, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .graph_utils import build_graph, update_with_realtime, dijkstra

from .models import (
    Agency, 
    FeedInfo,
    FareAttribute,
    FareRule,
    RiderCategory,
    FareRiderCategory,
    Route, 
    Stop, 
    Trip,
    Calendar,
    RouteAttribute,
    RealtimeRoute,
    Direction,
    StopTime,
    Transfer,
    Shape,
    CalendarAttribute,
    CalendarDate,
    RealtimeStopTimeUpdate,
    RealtimeAlert,
    RealtimeTrip,
)

from .serializers import (
    AgencySerializer, 
    FeedInfoSerializer,
    FareAttributeSerializer,
    FareRuleSerializer,
    RiderCategorySerializer,
    FareRiderCategorySerializer,
    ShapeSerializer,
    RouteSerializer,
    RouteAttributeSerializer,
    RealtimeRouteSerializer,
    DirectionSerializer, 
    StopSerializer, 
    StopTimeSerializer,
    TransferSerializer,
    CalendarSerializer,
    CalendarAttributeSerializer,
    CalendarDateSerializer, 
    TripSerializer, 
    RealtimeStopTimeUpdateSerializer,
    RealtimeAlertSerializer,
    RealtimeTripSerializer,

    RealtimeStopTimeUpdateSerializerForStopTimeUpdateView,
    RouteSummarySerializer,
    StopSummarySerializer,
    TripsSummarySerializer,
    RealtimeTripSummarySerializer,
    RealtimeStopTimeUpdateSummarySerializer,
)

# Homepage initial response
def home(request):
    return HttpResponse("Hello, world. You're at the BART app home page.")

# BART API test response - for testing purposes only
def get_departures(request):
    API_KEY = 'MW9S-E7SL-26DU-VV8V'
    BART_API_URL = f'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=all&key={API_KEY}&json=y'

    response = requests.get(BART_API_URL)  # Corrected this line to use the variable
    data = response.json()
    return JsonResponse(data)

# Test function to get all agencies from the database
def get_agencies(request):
    agencies = Agency.objects.all()
    return render(request, 'agency_list.html', {'agencies': agencies})

# Basic viewsets for each model
class AgencyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

class FeedInfoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FeedInfo.objects.all()
    serializer_class = FeedInfoSerializer

class FareAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FareAttribute.objects.all()
    serializer_class = FareAttributeSerializer

class FareRuleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FareRule.objects.all()
    serializer_class = FareRuleSerializer

class RiderCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RiderCategory.objects.all()
    serializer_class = RiderCategorySerializer

class FareRiderCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FareRiderCategory.objects.all()
    serializer_class = FareRiderCategorySerializer

class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class StopViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer

class TripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class CalendarViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class RouteAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RouteAttribute.objects.all()
    serializer_class = RouteAttributeSerializer

class RealtimeRouteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RealtimeRoute.objects.all()
    serializer_class = RealtimeRouteSerializer

class DirectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer

class StopTimeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer

class TransferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

class ShapeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer

class CalendarAttributeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalendarAttribute.objects.all()
    serializer_class = CalendarAttributeSerializer

class CalendarDateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CalendarDate.objects.all()
    serializer_class = CalendarDateSerializer

class RealtimeStopTimeUpdateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RealtimeStopTimeUpdate.objects.all()
    serializer_class = RealtimeStopTimeUpdateSerializer

class RealtimeAlertViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RealtimeAlert.objects.all()
    serializer_class = RealtimeAlertSerializer

class RealtimeTripViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RealtimeTrip.objects.all()
    serializer_class = RealtimeTripSerializer

# Provides current alerts -if no return, then no alerts.
class AlertInfoView(APIView):
    def get(self, request):
        alerts = RealtimeAlert.objects.values_list('info', flat=True)
        return Response(alerts)
    
# Requests fees for a to and from locations
class FareView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')

        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')
        date = request.query_params.get('date', 'today')
        api_url = f'https://api.bart.gov/api/sched.aspx?cmd=fare&orig={origin}&dest={destination}&date={date}&key={api_key}&json=y'

        response = requests.get(api_url)

        if response.status_code != 200:
            return Response({'error': 'Failed to fetch fare information from BART API'}, status=status.HTTP_502_BAD_GATEWAY)

        if not response.content:
            return Response({'error': 'Empty response from BART API'}, status=status.HTTP_502_BAD_GATEWAY)

        try:
            data = response.json().get('root').get('fares').get('fare')
        except ValueError:
            return Response({'error': 'Invalid JSON response from BART API'}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(data)

# Provides for route_short_name the total number of trains and the number of trains that are late
class LateTripsView(APIView):       
    def get(self, request):
        late_subquery = (
            RealtimeStopTimeUpdate.objects
            .select_related('trip_id__trip_id__route_id')
            .filter(
                arrival_delay__gt=0,
                trip_id__trip_id__route_id=OuterRef('pk')
            )
            .values('trip_id__trip_id__route_id')
            .annotate(count=Count('trip_id__trip_id', distinct=True))
            .values('count')
        )
        total_subquery = (
            RealtimeStopTimeUpdate.objects
            .select_related('trip_id__trip_id__route_id')
            .filter(
                trip_id__trip_id__route_id=OuterRef('pk')
            )
            .values('trip_id__trip_id__route_id')
            .annotate(count=Count('trip_id__trip_id', distinct=True))
            .values('count')
        )
        routes_with_counts = (
            Route.objects
            .annotate(
                late_count=Subquery(late_subquery),
                total_count=Subquery(total_subquery)
            )
            .filter(late_count__isnull=False)
            .values('route_short_name', 'late_count', 'total_count')
        )
        return Response(routes_with_counts)

# Please see the notes from the website for usage of this endpoint view: https://api.bart.gov/docs/bsa/bsa.aspx
# Requests current count of trains active in the system
class ActiveTrainsView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        api_url = f'https://api.bart.gov/api/bsa.aspx?cmd=count&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('traincount')

        return Response(data)

# Requests detailed information on the specified station such as what routes on which platforms
# Note: Returns for each platform route_ids only
class StationInfoView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        station = request.query_params.get('station', '24th')  # Default to '24th' if no station is provided
        api_url = f'https://api.bart.gov/api/stn.aspx?cmd=stninfo&orig={station}&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('stations').get('station')

        return Response(data)

# Please read notes from the website for usage of this endpoint view: https://api.bart.gov/docs/etd/etd.aspx
class StationRTInfoView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        station = request.query_params.get('station', '24th')  # Default to '24th' if no station is provided
        api_url = f'https://api.bart.gov/api/etd.aspx?cmd=etd&orig={station}&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('station')

        return Response(data)

# Requests for a station the schedule of routes for the day with time and trainheadstation name.
# Note: Returns for each the route_id for a schedule for a station. Not the route_short_name
class StationScheduleView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')

        orig = request.query_params.get('station')
        date = request.query_params.get('date', 'now')
        
        api_url = f'https://api.bart.gov/api/sched.aspx?cmd=stnsched&orig={orig}&key={api_key}&date={date}&json=y'
        
        response = requests.get(api_url)
        
        data = response.json()
        root = data.get('root')
        station_schedule = root.get('station')
        return Response(station_schedule)

# Requests advisory information on elevator status for all stations
class AdvisoryElevatorInfoView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        api_url = f'https://api.bart.gov/api/bsa.aspx?cmd=elev&key={api_key}&json=y'

        response = requests.get(api_url)
        data = response.json().get('root').get('bsa')

        return Response(data)

# Please see the full example from the website for usage of this endpoint view: https://api.bart.gov/docs/stn/stnaccess.aspx
# Requests advisory information on access to and from a station - includes parking, lockers, car_share etc.
class StationAccessView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        station = request.query_params.get('station', '24th')  # Default to '24th' if no station is provided
        api_url = f'https://api.bart.gov/api/stn.aspx?cmd=stnaccess&orig={station}&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('stations').get('station')

        return Response(data)

# Please read notes from the website for usage of this endpoint view: https://api.bart.gov/docs/sched/arrive.aspx
# Requests a trip based on arriving at the time specified. 
class ScheduleInfoArriveView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        if not api_key:
            return Response({"error": "API_KEY not found in environment variables"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        orig = request.query_params.get('orig')
        dest = request.query_params.get('dest')
        time = request.query_params.get('time', 'now')
        date = request.query_params.get('date', 'now')
        b = request.query_params.get('b', '2')
        a = request.query_params.get('a', '2')
        l = request.query_params.get('l', '0')
        
        if not orig or not dest:
            return Response({"error": "Both 'orig' and 'dest' parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            return Response({"error": "Invalid date format. Use MM/DD/YYYY."}, status=status.HTTP_400_BAD_REQUEST)

        api_url = f'https://api.bart.gov/api/sched.aspx?cmd=arrive&orig={orig}&dest={dest}&time={time}&date={date}&key={api_key}&b={b}&a={a}&l={l}&json=y'
        
        response = requests.get(api_url)
        
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from BART API"}, status=status.HTTP_502_BAD_GATEWAY)
        
        data = response.json()
        root = data.get('root')
        if not root:
            return Response({"error": "Invalid response structure: 'root' key missing"}, status=status.HTTP_502_BAD_GATEWAY)
        
        schedule = root.get('schedule')
        if not schedule:
            return Response({"error": "Invalid response structure: 'schedule' key missing"}, status=status.HTTP_502_BAD_GATEWAY)
        
        return Response(schedule)

# Please read notes from the website for usage of this endpoint view: https://api.bart.gov/docs/sched/depart.aspx
# Requests a trip based on departing at the time specified.
class ScheduleInfoDepartView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        if not api_key:
            return Response({"error": "API_KEY not found in environment variables"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        orig = request.query_params.get('orig')
        dest = request.query_params.get('dest')
        time = request.query_params.get('time', 'now')
        date = request.query_params.get('date', 'now')
        b = request.query_params.get('b', '2')
        a = request.query_params.get('a', '2')
        l = request.query_params.get('l', '0')

        if not orig or not dest:
            return Response({"error": "Both 'orig' and 'dest' parameters are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            datetime.strptime(date, "%m/%d/%Y")
        except ValueError:
            return Response({"error": "Invalid date format. Use MM/DD/YYYY."}, status=status.HTTP_400_BAD_REQUEST)

        api_url = f'https://api.bart.gov/api/sched.aspx?cmd=depart&orig={orig}&dest={dest}&time={time}&date={date}&key={api_key}&b={b}&a={a}&l={l}&json=y'

        response = requests.get(api_url)

        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from BART API"}, status=status.HTTP_502_BAD_GATEWAY)
        
        data = response.json()
        root = data.get('root')
        if not root:
            return Response({"error": "Invalid response structure: 'root' key missing"}, status=status.HTTP_502_BAD_GATEWAY)
        
        schedule = root.get('schedule')
        if not schedule:
            return Response({"error": "Invalid response structure: 'schedule' key missing"}, status=status.HTTP_502_BAD_GATEWAY)
        
        return Response(schedule)

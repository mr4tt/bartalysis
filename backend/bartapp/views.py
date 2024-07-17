from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
import requests

from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import api_view

from rest_framework import viewsets
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
    TrainSchedule,
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
    TrainScheduleSerializer,
)

from rest_framework import generics

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

def home(request):
    return HttpResponse("Hello, world. You're at the BART app home page.")

# Deprecated
def get_departures(request):
    API_KEY = 'MW9S-E7SL-26DU-VV8V'
    BART_API_URL = f'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=all&key={API_KEY}&json=y'

    response = requests.get(BART_API_URL)  # Corrected this line to use the variable
    data = response.json()
    return JsonResponse(data)

def get_agencies(request):
    agencies = Agency.objects.all()
    return render(request, 'agency_list.html', {'agencies': agencies})

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

class FeedInfoViewSet(viewsets.ModelViewSet):
    queryset = FeedInfo.objects.all()
    serializer_class = FeedInfoSerializer

class FareAttributeViewSet(viewsets.ModelViewSet):
    queryset = FareAttribute.objects.all()
    serializer_class = FareAttributeSerializer

class FareRuleViewSet(viewsets.ModelViewSet):
    queryset = FareRule.objects.all()
    serializer_class = FareRuleSerializer

class RiderCategoryViewSet(viewsets.ModelViewSet):
    queryset = RiderCategory.objects.all()
    serializer_class = RiderCategorySerializer

class FareRiderCategoryViewSet(viewsets.ModelViewSet):
    queryset = FareRiderCategory.objects.all()
    serializer_class = FareRiderCategorySerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class RouteAttributeViewSet(viewsets.ModelViewSet):
    queryset = RouteAttribute.objects.all()
    serializer_class = RouteAttributeSerializer

class RealtimeRouteViewSet(viewsets.ModelViewSet):
    queryset = RealtimeRoute.objects.all()
    serializer_class = RealtimeRouteSerializer

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer

class StopTimeViewSet(viewsets.ModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

class ShapeViewSet(viewsets.ModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer

class CalendarAttributeViewSet(viewsets.ModelViewSet):
    queryset = CalendarAttribute.objects.all()
    serializer_class = CalendarAttributeSerializer

class CalendarDateViewSet(viewsets.ModelViewSet):
    queryset = CalendarDate.objects.all()
    serializer_class = CalendarDateSerializer

class RealtimeStopTimeUpdateViewSet(viewsets.ModelViewSet):
    queryset = RealtimeStopTimeUpdate.objects.all()
    serializer_class = RealtimeStopTimeUpdateSerializer

    # def get(self, request, stop_id):
    #     realtime_stop_times = RealtimeStopTimeUpdate.objects.filter(stop_id=stop_id)
    #     serializer = RealtimeStopTimeUpdateSerializer(realtime_stop_times, many=True)
    #     return Response(serializer.data)

class RealtimeAlertViewSet(viewsets.ModelViewSet):
    queryset = RealtimeAlert.objects.all()
    serializer_class = RealtimeAlertSerializer

class RealtimeTripViewSet(viewsets.ModelViewSet):
    queryset = RealtimeTrip.objects.all()
    serializer_class = RealtimeTripSerializer














class IncomingTrainsView(APIView):
    def incoming_trains_view(request, station_id):
        user_time_str = request.GET.get('time')
        if not user_time_str:
            return JsonResponse({"error": "Time parameter is required"}, status=400)
        
        try:
            user_time = datetime.strptime(user_time_str, '%H:%M').time()
        except ValueError:
            return JsonResponse({"error": "Invalid time format. Use HH:MM"}, status=400)
        
        incoming_trains = TrainSchedule.objects.filter(
            station_id=station_id,
            arrival_time__gte=user_time
        ).order_by('arrival_time')[:3]

        serializer = TrainScheduleSerializer(incoming_trains, many=True)
        return Response(serializer.data)
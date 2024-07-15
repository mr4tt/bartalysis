from django.shortcuts import render

from django.http import JsonResponse
import requests

from rest_framework import viewsets
from .models import Agency, Route, Stop, StopTime, Calendar, Trip, TrainSchedule
from .serializers import AgencySerializer, RouteSerializer, StopSerializer, StopTimeSerializer, CalendarSerializer, TripSerializer, RealtimeStopTimeUpdateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

def get_departures(request):
    API_KEY = 'MW9S-E7SL-26DU-VV8V'
    BART_API_URL = f'http://api.bart.gov/api/etd.aspx?cmd=etd&orig=all&key={API_KEY}&json=y'

    response = requests.get(BART_API_URL)  # Corrected this line to use the variable
    data = response.json()
    return JsonResponse(data)

def get_agencies(request):
    agencies = Agency.objects.all()
    return render(request, 'agency_list.html', {'agencies': agencies})

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer

class StopViewSet(viewsets.ModelViewSet):
    queryset = Stop.objects.all()
    serializer_class = StopSerializer

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class StopTimeViewSet(viewsets.ModelViewSet):
    queryset = StopTime.objects.all()
    serializer_class = StopTimeSerializer

class AgencyViewSet(viewsets.ModelViewSet):
    queryset = Agency.objects.all()
    serializer_class = AgencySerializer

class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarSerializer

class FeedInfoViewSet(viewsets.ModelViewSet):
    queryset = FeedInfo.objects.all()
    serializer_class = FeedInfoSerializer

class RealtimeStopTimeUpdateView(APIView):
    def get(self, request):
        updates = RealtimeStopTimeUpdate.objects.all()
        serializer = RealtimeStopTimeUpdateSerializer(updates, many=True)
        return Response(serializer.data)

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
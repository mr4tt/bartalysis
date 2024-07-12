from django.shortcuts import render

from django.http import JsonResponse
import requests

from rest_framework import viewsets
from .models import Route, Stop, Trip, StopTime, Agency, Calendar
from .serializers import RouteSerializer, StopSerializer, TripSerializer, StopTimeSerializer, AgencySerializer, CalendarSerializer

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


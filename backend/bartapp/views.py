import requests
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.db import connections

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
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

# Non-Generic Views
class RoutePlannerView(APIView):
    def get(self, request, start_station, end_station):
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        
        if not date or not time:
            return Response({"error": "Date and time are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Parse the date and determine the day of the week
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A").lower()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Map day of the week to corresponding column in the calendar table
        day_column = {
            'monday': 'c.monday',
            'tuesday': 'c.tuesday',
            'wednesday': 'c.wednesday',
            'thursday': 'c.thursday',
            'friday': 'c.friday',
            'saturday': 'c.saturday',
            'sunday': 'c.sunday'
        }.get(day_of_week, None)
        
        if not day_column:
            return Response({"error": "Invalid day of the week."}, status=status.HTTP_400_BAD_REQUEST)

        # Query for incoming trains
        train_query = f"""
        SELECT DISTINCT
            r.route_short_name AS TrainName, 
            r.route_color AS TrainColor, 
            r.route_long_name AS TrainDescription,
            st1.stop_id AS StartingID, 
            st2.stop_id AS EndingID, 
            st1.departure_time AS DepartureTime, 
            st2.arrival_time AS ArrivalTime
        FROM trips t
        JOIN stop_times st1 ON t.trip_id = st1.trip_id AND st1.stop_id = %s
        JOIN stop_times st2 ON t.trip_id = st2.trip_id AND st2.stop_id = %s
        JOIN routes r ON t.route_id = r.route_id
        JOIN calendar c ON t.service_id = c.service_id
        WHERE {day_column} = 1
        AND st1.departure_time > %s
        AND st1.stop_sequence < st2.stop_sequence
        AND %s BETWEEN c.start_date AND c.end_date
        ORDER BY st1.departure_time;
        """
        
        # Query for fare information
        fare_query = """
        SELECT DISTINCT FareID, Price, Description
        FROM (
            SELECT
                fa.fare_id AS FareID,
                fa.price AS Price,
                'Regular' AS Description
            FROM fare_attributes fa
            WHERE fa.fare_id IN (
                SELECT fare_id FROM fare_rules
                WHERE origin_id = %s
                AND destination_id = %s
            )

            UNION ALL

            SELECT
                frc.fare_id AS FareID,
                frc.price AS Price,
                rc.rider_category_description AS Description
            FROM fare_rider_categories frc
            JOIN rider_categories rc ON frc.rider_category_id = rc.rider_category_id
            WHERE frc.fare_id IN (
                SELECT fare_id FROM fare_rules
                WHERE origin_id = %s
                AND destination_id = %s
            )
        ) ORDER BY FareID, Description;
        """

        with connections['bart'].cursor() as cursor:
            # Execute train query
            cursor.execute(train_query, [start_station, end_station, time, date])
            train_rows = cursor.fetchall()
            
            # Execute fare query
            cursor.execute(fare_query, [start_station, end_station, start_station, end_station])
            fare_rows = cursor.fetchall()
        
        trains = [
            {
                "TrainName": row[0],
                "TrainColor": row[1],
                "TrainDescription": row[2],
                "StartingID": row[3],
                "EndingID": row[4],
                "DepartureTime": row[5],
                "ArrivalTime": row[6]
            }
            for row in train_rows
        ]
        
        fares = [
            {
                "FareID": row[0],
                "Price": row[1],
                "Description": row[2]
            }
            for row in fare_rows
        ]
        
        response_data = {
            "trains": trains,
            "fares": fares
        }

        return Response(response_data, status=status.HTTP_200_OK)
    
class AlertInfoView(APIView):
    def get(self, request):
        alerts = RealtimeAlert.objects.values_list('info', flat=True)
        return Response(alerts)
    
class FareView(APIView):
    def get(self, request, category, origin, destination):
        fare = FareAttribute.objects.select_related('farerule'
        ).select_related('fareridercategory'
        ).filter(fareridercategory__rider_category_id=category, farerule__origin_id=origin, farerule__destination_id=destination, 
        ).values_list('price', flat=True)
        return Response(fare)

class StopTimeUpdateView(APIView):
    def get(self, request, **kwargs):
        stop_id = self.kwargs['stop_id']
        if stop_id is not None:
            stop_time_updates = RealtimeStopTimeUpdate.objects.filter(stop_id=stop_id)
        else:
            return Response({'error': 'stop_id is required'}, status=400)
        serializer = RealtimeStopTimeUpdateSerializer(stop_time_updates, many=True)
        return Response(serializer.data)

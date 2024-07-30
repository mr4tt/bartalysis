import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.db import connection, connections
from django.utils import timezone
from django.db.models import F, OuterRef, Subquery, Count

# import pytz

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
    # LateTripsViewSerializer,
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

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Non-Generic Views
class RoutePlannerView(APIView):
    def get(self, request, start_station, end_station):
        # logger.debug("Using RoutePlannerView")
        # logger.debug("Received request with start_station: %s, end_station: %s", start_station, end_station)
        
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        # logger.debug("Received date: %s and time: %s", date, time)

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

        # logger.debug("Planning direct route from %s to %s", start_station, end_station)
        # logger.debug("Query Parameters: %s, %s, %s, %s", start_station, end_station, time, date)

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
        
        # logger.debug("Executing direct route query: %s", train_query)
        # logger.debug("Query Parameters: %s, %s, %s, %s", start_station, end_station, time, date)
        
        with connections['bart'].cursor() as cursor:
            # Execute train query
            cursor.execute(train_query, [start_station, end_station, time, date])
            train_rows = cursor.fetchall()
            
            # Execute fare query
            cursor.execute(fare_query, [start_station, end_station, start_station, end_station])
            fare_rows = cursor.fetchall()
        
        # logger.debug("Direct route query result: %s", train_rows)

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

# class RoutePlannerView2(APIView):
#     def get(self, request, start_station, end_station):
#         date = request.query_params.get('date')
#         time = request.query_params.get('time')

#         if not date or not time:
#             return Response({"error": "Date and time are required"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             date_obj = datetime.strptime(date, "%Y-%m-%d")
#             day_of_week = date_obj.strftime("%A").lower()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

#         day_column = {
#             'monday': 'monday',
#             'tuesday': 'tuesday',
#             'wednesday': 'wednesday',
#             'thursday': 'thursday',
#             'friday': 'friday',
#             'saturday': 'saturday',
#             'sunday': 'sunday'
#         }.get(day_of_week, None)

#         if not day_column:
#             return Response({"error": "Invalid day of the week."}, status=status.HTTP_400_BAD_REQUEST)

#         # Query for incoming trains
#         trains = Trip.objects.filter(
#             stoptime__stop_id=start_station,
#             stoptime__departure_time__gt=time,
#             stoptime__trip_id=F('trip_id'),
#             stoptime__stop_sequence__lt=F('stoptime__stop_sequence'),
#             service_id__in=Calendar.objects.filter(
#                 start_date__lte=date,
#                 end_date__gte=date,
#                 **{day_column: True}
#             ).values('service_id')
#         ).values(
#             TrainName=F('route_id__route_short_name'),
#             TrainColor=F('route_id__route_color'),
#             TrainDescription=F('route_id__route_long_name'),
#             StartingID=F('stoptime__stop_id'),
#             EndingID=F('stoptime__stop_id'),
#             DepartureTime=F('stoptime__departure_time'),
#             ArrivalTime=F('stoptime__arrival_time')
#         ).distinct()

#         # Query for fare information
#         fare_rules = FareRule.objects.filter(
#             origin_id=start_station,
#             destination_id=end_station
#         ).values_list('fare_id', flat=True)

#         # Perform the queries separately
#         fare_attributes = FareAttribute.objects.filter(
#             fare_id__in=fare_rules
#         ).values(
#             FareID=F('fare_id'),
#             Price=F('price'),
#             Description=F('fare_id')
#         )

#         fare_rider_categories = FareRiderCategory.objects.filter(
#             fare_id__in=fare_rules
#         ).values(
#             FareID=F('fare_id'),
#             Price=F('price'),
#             Description=F('rider_category_id__rider_category_description')
#         )

#         # Combine the results
#         combined_fares = list(fare_attributes) + list(fare_rider_categories)

#         # Remove duplicates based on FareID
#         unique_fares = {fare['FareID']: fare for fare in combined_fares}.values()

#         response_data = {
#             "trains": list(trains),
#             "fares": list(unique_fares)
#         }

#         return Response(response_data, status=status.HTTP_200_OK)

def normalize_time(time_str):
    """Normalize time strings that exceed 24 hours."""
    hours, minutes, seconds = map(int, time_str.split(':'))
    if hours >= 24:
        hours -= 24
        return f"{hours:02}:{minutes:02}:{seconds:02}", True
    return time_str, False

class PlanRouteView(APIView):

    def get(self, request, start_station, end_station):
        
        date = request.query_params.get('date')
        time = request.query_params.get('time')
        
        if not date or not time:
            return Response({"error": "Date and time are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            day_of_week = date_obj.strftime("%A").lower()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
        
        result = self.main_route_planner(start_station, end_station, date, time, day_of_week)
        
        return Response(result, status=status.HTTP_200_OK if "trains" in result else status.HTTP_400_BAD_REQUEST)

    def main_route_planner(self, start_station, end_station, date, time, day_of_week):
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
            return {"error": "Invalid day of the week"}

        direct_route = self.plan_route(start_station, end_station, date, time, day_column)
        
        if direct_route["trains"]:
            return direct_route
        
        transfer_routes = self.find_transfer_routes(start_station, end_station, date, time, day_column)
        
        if transfer_routes:
            sorted_transfer_routes = self.filter_and_sort_routes(transfer_routes["trains"], time)
            return sorted_transfer_routes

        return {"error": "No available routes found"}

    def plan_route(self, start_station, end_station, date, time, day_column):

        start_time_obj = datetime.strptime(time, "%H:%M:%S")
        one_hour_after_start_time = (start_time_obj + timedelta(hours=1)).strftime("%H:%M:%S")

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
        AND st1.departure_time < %s
        AND st1.stop_sequence < st2.stop_sequence
        AND %s BETWEEN c.start_date AND c.end_date
        ORDER BY st1.departure_time;
        """
        
        with connections['bart'].cursor() as cursor:
            cursor.execute(train_query, [start_station, end_station, time, one_hour_after_start_time, date])
            train_rows = cursor.fetchall()

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
        
        return {"trains": trains} if trains else {"trains": []}

    def find_transfer_routes(self, start_station, end_station, date, time, day_column):
        transfer_query = f"""
        SELECT DISTINCT
            tr.from_stop_id AS TransferID,
            COALESCE(tr.min_transfer_time, 1) AS TransferTime
        FROM transfers tr;
        """
        
        with connections['bart'].cursor() as cursor:
            cursor.execute(transfer_query)
            transfer_rows = cursor.fetchall()
        
        transfer_routes = []
        for row in transfer_rows:
            transfer_station = row[0]
            min_transfer_time = row[1]

            first_leg_routes = self.plan_route(start_station, transfer_station, date, time, day_column)
            for first_leg in first_leg_routes["trains"]:
                arrival_time = first_leg["ArrivalTime"]
                normalized_arrival_time, next_day = normalize_time(arrival_time)
                adjusted_datetime = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), datetime.strptime(normalized_arrival_time, "%H:%M:%S").time()) + timedelta(minutes=min_transfer_time)
                if next_day:
                    adjusted_datetime += timedelta(days=1)
                adjusted_time = adjusted_datetime.time()
                second_leg_routes = self.plan_route(transfer_station, end_station, date, adjusted_time.strftime("%H:%M:%S"), day_column)
                for second_leg in second_leg_routes["trains"]:
                    transfer_routes.append({
                        "first_leg": first_leg,
                        "second_leg": second_leg
                    })

        return {"trains": transfer_routes} if transfer_routes else {}

    def reroute_from_transfer(self, transfer_station, end_station, transfer_time, date, day_column):
        logger.debug("Using reroute_from_transfer")
        logger.debug("Rerouting from transfer station %s to %s", transfer_station, end_station)
        reroute_query = f"""
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
        
        logger.debug("Query Parameters: %s, %s, %s, %s", transfer_station, end_station, transfer_time, date)
        
        with connections['bart'].cursor() as cursor:
            cursor.execute(reroute_query, [transfer_station, end_station, transfer_time, date])
            reroute_rows = cursor.fetchall()
        
        return [
            {
                "TrainName": row[0],
                "TrainColor": row[1],
                "TrainDescription": row[2],
                "StartingID": row[3],
                "EndingID": row[4],
                "DepartureTime": row[5],
                "ArrivalTime": row[6]
            }
            for row in reroute_rows
        ]

    def filter_and_sort_routes(self, routes, start_time):
        
        # Parse the start time and calculate the next 60-minute increment
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S")
        start_time_only = start_time_obj.time()
        next_60_min_increment = (start_time_obj + timedelta(minutes=60)).time()

        filtered_trains = []

        # Iterate over each route
        for route in routes:
            first_leg = route.get("first_leg", {})
            second_leg = route.get("second_leg", {})
            
            # Extract the departure time of the first leg and the arrival time of the second leg
            first_leg_departure = first_leg.get("DepartureTime")
            second_leg_arrival = second_leg.get("ArrivalTime")
            
            if first_leg_departure and second_leg_arrival:
                # Convert these times to datetime objects
                first_leg_departure_obj = datetime.strptime(first_leg_departure, "%H:%M:%S").time()
                second_leg_arrival_obj = datetime.strptime(second_leg_arrival, "%H:%M:%S").time()
                
                # Check if the first leg departure time is within the 60-minute window
                if start_time_only <= first_leg_departure_obj < next_60_min_increment:
                    # Calculate the total trip time
                    first_leg_departure_dt = datetime.strptime(first_leg_departure, "%H:%M:%S")
                    second_leg_arrival_dt = datetime.strptime(second_leg_arrival, "%H:%M:%S")
                    total_trip_time = (second_leg_arrival_dt - first_leg_departure_dt).total_seconds()
                    
                    # Add the route to the filtered list with total trip time
                    route["total_trip_time"] = total_trip_time
                    filtered_trains.append(route)

            else:
                # Log an error if keys are missing
                logger.error("Missing 'DepartureTime' or 'ArrivalTime' in route: %s", route)

        # Sort the filtered trains first by total trip time and then by second leg arrival time
        sorted_trains = sorted(filtered_trains, key=lambda x: (x["total_trip_time"], datetime.strptime(x["second_leg"]["ArrivalTime"], "%H:%M:%S").time()))
        
        # Find the minimum total trip time
        if sorted_trains:
            min_total_trip_time = sorted_trains[0]["total_trip_time"]
            # Filter the trains to include only those with the minimum total trip time
            top_trains = [train for train in sorted_trains if train["total_trip_time"] == min_total_trip_time]
        else:
            top_trains = []

        return {"trains": top_trains}

class AlertInfoView(APIView):
    def get(self, request):
        alerts = RealtimeAlert.objects.values_list('info', flat=True)
        return Response(alerts)
    
class FareView(APIView):
    def get(self, request):
        category = request.query_params.get('category')
        origin = request.query_params.get('origin')
        destination = request.query_params.get('destination')

        if not category or not origin or not destination:
            return Response({'error': 'category, origin, and destination are required'}, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = RealtimeStopTimeUpdateSerializerForStopTimeUpdateView(stop_time_updates, many=True)
        return Response(serializer.data)
        
class ServiceInfoView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        api_url = f'https://api.bart.gov/api/bsa.aspx?cmd=count&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('traincount')

        return Response(data)
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
            .values('route_id', 'late_count', 'total_count')
        )

        return Response(routes_with_counts)

class ActiveTrainsView(APIView):
    def get(self, request):
        load_dotenv()
        api_key = os.getenv('API_KEY')
        api_url = f'https://api.bart.gov/api/bsa.aspx?cmd=count&key={api_key}&json=y'
        
        response = requests.get(api_url)
        data = response.json().get('root').get('traincount')

        return Response(data)

from rest_framework import serializers

from .models import (
    Agency, 
    FeedInfo, 
    FareAttribute, 
    FareRule, 
    RiderCategory, 
    FareRiderCategory, 
    Shape, 
    Route, 
    RouteAttribute, 
    RealtimeRoute, 
    Direction, 
    Stop, 
    StopTime, 
    Transfer, 
    Calendar, 
    CalendarAttribute, 
    CalendarDate, 
    Trip, 
    RealtimeStopTimeUpdate, 
    RealtimeAlert, 
    RealtimeTrip,
)

class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = '__all__'

class FeedInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedInfo
        fields = '__all__'

class FareAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FareAttribute
        fields = '__all__'

class FareRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FareRule
        fields = '__all__'

class RiderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RiderCategory
        fields = '__all__'

class FareRiderCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FareRiderCategory
        fields = '__all__'

class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class RouteAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteAttribute
        fields = '__all__'

class RealtimeRouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeRoute
        fields = '__all__'

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class StopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = '__all__'

class StopTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StopTime
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = '__all__'

class CalendarAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarAttribute
        fields = '__all__'

class CalendarDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalendarDate
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class RealtimeStopTimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeStopTimeUpdate
        fields = '__all__'

class RealtimeAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeAlert
        fields = '__all__'

class RealtimeTripSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeTrip
        fields = '__all__'


# Specific serializers

class RealtimeStopTimeUpdateSerializerForStopTimeUpdateView(serializers.ModelSerializer):
    class Meta:
        model = RealtimeStopTimeUpdate
        fields = ['arrival_uncertainty', 'departure_delay', 'departure_time', 'departure_uncertainty']

class RouteSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_short_name', 'route_long_name', 'route_color']

class StopSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Stop
        fields = ['stop_id', 'stop_name']

class TripsSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['trip_id', 'route_id', 'service_id', 'direction_id']

class RealtimeTripSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeTrip
        fields = ['trip_id', 'schedule_relationship', 'vehicle']

class RealtimeStopTimeUpdateSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = RealtimeStopTimeUpdate
        fields = ['arrival_uncertainty', 'arrival_time', 'departure_delay', 'departure_time', 'departure_uncertainty', 'stop_id', 'trip_id']

class RouteSpecificSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'route_short_name', 'route_long_name', 'route_color']
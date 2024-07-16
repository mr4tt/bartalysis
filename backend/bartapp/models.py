from django.db import models

# Models for all GTFS tables

class Agency(models.Model):
    agency_id = models.TextField(primary_key=True)
    agency_name = models.TextField()
    agency_url = models.URLField()
    agency_timezone = models.TextField(null=True)
    agency_lang = models.TextField(null=True)
    agency_phone = models.TextField()

    class Meta:
        db_table = 'agency'

    def __str__(self):
        return self.agency_name

class FeedInfo(models.Model):
    feed_publisher_name = models.TextField()
    feed_publisher_url = models.URLField()
    feed_lang = models.TextField()
    feed_start_date = models.DateField()
    feed_end_date = models.DateField()
    feed_version = models.TextField()

    class Meta:
        db_table = 'feed_info'

    def __str__(self):
        return self.feed_publisher_name

class FareAttribute(models.Model):
    fare_id = models.IntegerField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_type = models.TextField()
    payment_method = models.IntegerField()
    transfers = models.IntegerField(null=True)
    transfer_duration = models.IntegerField(null=True)

    class Meta:
        db_table = 'fare_attributes'

    def __str__(self):
        return self.fare_id

class FareRule(models.Model):
    fare_id = models.OneToOneField(FareAttribute, on_delete=models.CASCADE, primary_key=True, db_column='fare_id')
    route_id = models.TextField(null=True)
    origin_id = models.TextField()
    destination_id = models.TextField()
    contains_id = models.TextField(null=True)

    class Meta:
        db_table = 'fare_rules'

class RiderCategory(models.Model):
    rider_category_id = models.IntegerField(primary_key=True)
    rider_category_description = models.TextField()

    class Meta:
        db_table = 'rider_categories'

    def __str__(self):
        return self.rider_category_id

class FareRiderCategory(models.Model):
    fare_id = models.ForeignKey(FareAttribute, on_delete=models.CASCADE, db_column='fare_id')
    rider_category_id = models.ForeignKey(RiderCategory, on_delete=models.CASCADE, db_column='rider_category_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'fare_rider_categories'

class Route(models.Model):
    route_id = models.TextField(primary_key=True)
    route_short_name = models.TextField()
    route_long_name = models.TextField(null=True)
    route_desc = models.TextField()
    route_type = models.IntegerField()
    route_url = models.URLField(null=True)
    route_color = models.TextField()
    route_text_color = models.TextField()

    class Meta:
        db_table = 'routes'

    def __str__(self):
        return self.route_long_name

class Stop(models.Model):
    stop_id = models.TextField(primary_key=True)
    stop_code = models.TextField(null=True)
    stop_name = models.TextField()
    stop_desc = models.TextField(null=True)
    stop_lat = models.TextField()
    stop_lon = models.TextField()
    zone_id = models.TextField(null=True)
    plc_url = models.URLField(null=True)
    location_type = models.IntegerField()
    parent_station = models.TextField(null=True)

    class Meta:
        db_table = 'stops'

    def __str__(self):
        return self.stop_name

class Trip(models.Model):
    route_id = models.TextField(null=True)
    service_id = models.TextField(null=True)
    trip_id = models.IntegerField(primary_key=True)
    trip_headsign = models.TextField()
    direction_id = models.TextField()
    block_id = models.TextField()
    shape_id = models.TextField()

    class Meta:
        db_table = 'trips'

class Calendar(models.Model):
    service_id = models.TextField(primary_key=True)
    monday = models.IntegerField()
    tuesday = models.IntegerField()
    wednesday = models.IntegerField()
    thursday = models.IntegerField()
    friday = models.IntegerField()
    saturday = models.IntegerField()
    sunday = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'calendar'

class RouteAttribute(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='route_id')
    category = models.TextField()
    subcategory = models.TextField()
    running_way = models.TextField()

    class Meta:
        db_table = 'route_attributes'

class RealtimeRoute(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='route_id')
    realtime_enabled = models.BooleanField()
    realtime_routename = models.TextField(null=True)
    realtime_routecode = models.TextField(null=True)

    class Meta:
        db_table = 'realtime_routes'

class Direction(models.Model):
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE, db_column='route_id')
    direction_id = models.TextField()
    direction = models.TextField()

    class Meta:
        db_table = 'directions'

class StopTime(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, db_column='trip_id')
    arrival_time = models.TextField()
    departure_time = models.TextField()
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE, db_column='stop_id')
    stop_sequence = models.IntegerField(null=True)
    stop_headsign = models.TextField(null=True)
    pickup_type = models.IntegerField(null=True)
    drop_off_type = models.IntegerField(null=True)
    shape_distance_traveled = models.IntegerField()

    class Meta:
        db_table = 'stop_times'

class Transfer(models.Model):
    from_stop_id = models.TextField()
    to_stop_id = models.TextField()
    transfer_type = models.IntegerField(null=True)
    min_transfer_time = models.IntegerField(null=True)
    from_route_id = models.TextField(null=True)
    to_route_id = models.TextField(null=True)
    from_trip_id = models.TextField(null=True)
    to_trip_id = models.TextField(null=True)

    class Meta:
        db_table = 'transfers'

class Shape(models.Model):
    shape_id = models.ForeignKey(Trip, on_delete=models.CASCADE, db_column='shape_id')
    shape_pt_lat = models.IntegerField()
    shape_pt_lon = models.IntegerField()
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.IntegerField()

    class Meta:
        db_table = 'shapes'


class CalendarAttribute(models.Model):
    service_id = models.OneToOneField(Calendar, on_delete=models.CASCADE, primary_key=True, db_column='service_id')
    service_description = models.TextField(max_length=255)

    class Meta:
        db_table = 'calendar_attributes'

class CalendarDate(models.Model):
    service_id = models.ForeignKey(Calendar, on_delete=models.CASCADE, db_column='service_id')
    date = models.DateField()
    exception_type = models.IntegerField()

    class Meta:
        db_table = 'calendar_dates'

class RealtimeStopTimeUpdate(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, db_column='trip_id')
    stop_id = models.ForeignKey(Stop, on_delete=models.CASCADE, db_column='stop_id')
    arrival_delay = models.IntegerField()
    arrival_time = models.IntegerField()
    arrival_uncertainty = models.IntegerField()
    departure_delay = models.IntegerField()
    departure_time = models.IntegerField()
    departure_uncertainty = models.IntegerField()

    class Meta:
        db_table = 'realtime_stop_time_updates'

class RealtimeAlert(models.Model):
    alert_id = models.IntegerField(primary_key=True)
    info = models.TextField()
    lang = models.TextField()

    class Meta:
        db_table = 'realtime_alerts'

class RealtimeTrip(models.Model):
    trip_id = models.ForeignKey(Trip, on_delete=models.CASCADE, db_column='trip_id')
    schedule_relationship = models.TextField()
    vehicle = models.TextField()

    class Meta:
        db_table = 'realtime_trips'

# Models for specific use cases
class TrainSchedule(models.Model):
    train_id = models.IntegerField()
    station_id = models.IntegerField()
    arrival_time = models.TimeField()
from django.db import models

class Agency(models.Model):
    agency_id = models.CharField(max_length=100, primary_key=True)
    agency_name = models.CharField(max_length=100)
    agency_url = models.URLField()
    agency_timezone = models.CharField(max_length=50, null=True, blank=True)
    agency_lang = models.CharField(max_length=10, null=True, blank=True)
    agency_phone = models.CharField(max_length=20)

    class Meta:
        db_table = 'agency'

    def __str__(self):
        return self.agency_name

class FeedInfo(models.Model):
    feed_publisher_name = models.CharField(max_length=100)
    feed_publisher_url = models.URLField()
    feed_lang = models.CharField(max_length=10)
    feed_start_date = models.DateField()
    feed_end_date = models.DateField()
    feed_version = models.CharField(max_length=20)

    class Meta:
        db_table = 'feed_info'

    def __str__(self):
        return self.feed_publisher_name

class FareAttribute(models.Model):
    fare_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency_type = models.CharField(max_length=3)
    payment_method = models.IntegerField()
    transfers = models.IntegerField()
    transfer_duration = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'fare_attributes'

    def __str__(self):
        return self.fare_id

class FareRule(models.Model):
    fare_id = models.CharField(max_length=100)
    route_id = models.CharField(max_length=100, null=True, blank=True)
    origin_id = models.CharField(max_length=100, null=True, blank=True)
    destination_id = models.CharField(max_length=100, null=True, blank=True)
    contains_id = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'fare_rules'

class RiderCategory(models.Model):
    rider_category_id = models.CharField(max_length=100, primary_key=True)
    rider_category_description = models.CharField(max_length=255)

    class Meta:
        db_table = 'rider_categories'

    def __str__(self):
        return self.rider_category_id

class FareRiderCategory(models.Model):
    fare_id = models.CharField(max_length=100)
    rider_category_id = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'fare_rider_categories'

class Shape(models.Model):
    shape_id = models.CharField(max_length=100)
    shape_pt_lat = models.FloatField()
    shape_pt_lon = models.FloatField()
    shape_pt_sequence = models.IntegerField()
    shape_dist_traveled = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'shapes'

class Route(models.Model):
    route_id = models.CharField(max_length=100, primary_key=True)
    route_short_name = models.CharField(max_length=50, null=True, blank=True)
    route_long_name = models.CharField(max_length=255)
    route_desc = models.CharField(max_length=255, null=True, blank=True)
    route_type = models.IntegerField()
    route_url = models.URLField(null=True, blank=True)
    route_color = models.CharField(max_length=10, null=True, blank=True)
    route_text_color = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'routes'

    def __str__(self):
        return self.route_long_name

class RouteAttribute(models.Model):
    route_id = models.CharField(max_length=100)
    category = models.CharField(max_length=50, null=True, blank=True)
    subcategory = models.CharField(max_length=50, null=True, blank=True)
    running_way = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'route_attributes'

class RealtimeRoute(models.Model):
    route_id = models.CharField(max_length=100)
    realtime_enabled = models.BooleanField()
    realtime_routename = models.CharField(max_length=100, null=True, blank=True)
    realtime_routecode = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'realtime_routes'

class Direction(models.Model):
    route_id = models.CharField(max_length=100)
    direction_id = models.CharField(max_length=50)
    direction = models.CharField(max_length=100)

    class Meta:
        db_table = 'directions'

class Stop(models.Model):
    stop_id = models.CharField(max_length=100, primary_key=True)
    stop_code = models.CharField(max_length=50, null=True, blank=True)
    stop_name = models.CharField(max_length=255)
    stop_desc = models.CharField(max_length=255, null=True, blank=True)
    stop_lat = models.FloatField()
    stop_lon = models.FloatField()
    zone_id = models.CharField(max_length=50, null=True, blank=True)
    plc_url = models.URLField(null=True, blank=True)
    location_type = models.IntegerField(null=True, blank=True)
    parent_station = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'stops'

    def __str__(self):
        return self.stop_name

class StopTime(models.Model):
    trip_id = models.CharField(max_length=100)
    arrival_time = models.CharField(max_length=20)
    departure_time = models.CharField(max_length=20)
    stop_id = models.CharField(max_length=100)
    stop_sequence = models.IntegerField()
    stop_headsign = models.CharField(max_length=255, null=True, blank=True)
    pickup_type = models.IntegerField(null=True, blank=True)
    drop_off_type = models.IntegerField(null=True, blank=True)
    shape_distance_traveled = models.FloatField(null=True, blank=True)

    class Meta:
        db_table = 'stop_times'

class Transfer(models.Model):
    from_stop_id = models.CharField(max_length=100)
    to_stop_id = models.CharField(max_length=100)
    transfer_type = models.IntegerField()
    min_transfer_time = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'transfers'

class Calendar(models.Model):
    service_id = models.CharField(max_length=100, primary_key=True)
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

class CalendarAttribute(models.Model):
    service_id = models.CharField(max_length=100)
    service_description = models.CharField(max_length=255)

    class Meta:
        db_table = 'calendar_attributes'

class CalendarDate(models.Model):
    service_id = models.CharField(max_length=100)
    date = models.DateField()
    exception_type = models.IntegerField()

    class Meta:
        db_table = 'calendar_dates'

class Trip(models.Model):
    route_id = models.CharField(max_length=100)
    service_id = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100, primary_key=True)
    trip_headsign = models.CharField(max_length=255, null=True, blank=True)
    direction_id = models.CharField(max_length=50, null=True, blank=True)
    block_id = models.CharField(max_length=50, null=True, blank=True)
    shape_id = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'trips'

class RTStopTimeUpdate(models.Model):
    trip_id = models.IntegerField()
    stop_id = models.CharField()
    arrival_delay = models.IntegerField()
    arrival_time = models.IntegerField()
    arrival_uncertainty = models.IntegerField()
    departure_delay = models.IntegerField()
    departure_time = models.IntegerField()
    departure_uncertainty = models.IntegerField()

    class Meta:
        db_table = 'rt_stop_time_updates'

class RTAlert(models.Model):
    alert_id = models.IntegerField(primary_key=True)
    info = models.CharField()
    lang = models.CharField()

    class Meta:
        db_table = 'rt_alerts'

class RTTrip(models.Model):
    trip_id = models.IntegerField(primary_key=True)
    schedule_relationship = models.CharField()
    vehicle = models.CharField()

    class Meta:
        db_table = 'rt_trips'
from django.test import TestCase, Client
from django.urls import reverse
from .models import Agency, Route, Trip, Stop, Calendar, RealtimeStopTimeUpdate, RealtimeAlert, RealtimeTrip, trainschedule

class EndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_agency_list(self):
        response = self.client.get(reverse('agency-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "agency_id")
        self.assertContains(response, "agency_name")

    def test_feed_info_list(self):
        response = self.client.get(reverse('feedinfo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "feed_publisher_name")
        self.assertContains(response, "feed_lang")

    def test_fare_attribute_list(self):
        response = self.client.get(reverse('fareattribute-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fare_id")
        self.assertContains(response, "price")

    def test_fare_rule_list(self):
        response = self.client.get(reverse('farerule-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fare_id")
        self.assertContains(response, "route_id")

    def test_rider_category_list(self):
        response = self.client.get(reverse('ridercategory-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "rider_category_id")
        self.assertContains(response, "rider_category_description")

    def test_fare_rider_category_list(self):
        response = self.client.get(reverse('fareridercategory-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "fare_id")
        self.assertContains(response, "rider_category_id")

    def test_shape_list(self):
        response = self.client.get(reverse('shape-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "shape_id")
        self.assertContains(response, "shape_pt_lat")

    def test_route_list(self):
        response = self.client.get(reverse('route-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route_id")
        self.assertContains(response, "route_long_name")

    def test_route_attribute_list(self):
        response = self.client.get(reverse('routeattribute-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route_id")
        self.assertContains(response, "category")

    def test_realtime_route_list(self):
        response = self.client.get(reverse('realtimeroute-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route_id")
        self.assertContains(response, "realtime_enabled")

    def test_direction_list(self):
        response = self.client.get(reverse('direction-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "route_id")
        self.assertContains(response, "direction_id")

    def test_stop_list(self):
        response = self.client.get(reverse('stop-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "stop_id")
        self.assertContains(response, "stop_name")

    def test_stop_time_list(self):
        response = self.client.get(reverse('stoptime-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "stop_id")

    def test_transfer_list(self):
        response = self.client.get(reverse('transfer-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "from_stop_id")
        self.assertContains(response, "to_stop_id")

    def test_calendar_list(self):
        response = self.client.get(reverse('calendar-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "service_id")
        self.assertContains(response, "monday")

    def test_calendar_attribute_list(self):
        response = self.client.get(reverse('calendarattribute-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "service_id")
        self.assertContains(response, "service_description")

    def test_calendar_date_list(self):
        response = self.client.get(reverse('calendardate-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "service_id")
        self.assertContains(response, "date")

    def test_trip_list(self):
        response = self.client.get(reverse('trip-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "route_id")

    def test_rt_stop_time_update_list(self):
        response = self.client.get(reverse('rtstoptimeupdate-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "stop_id")

    def test_rt_alert_list(self):
        response = self.client.get(reverse('rtalert-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alert_id")
        self.assertContains(response, "info")

    def test_rt_trip_list(self):
        response = self.client.get(reverse('rttrip-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "schedule_relationship")

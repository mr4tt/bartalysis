from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import (
    Agency,
    RealtimeAlert,
    Stop,
    Trip,
    RealtimeStopTimeUpdate
)

class EndpointTestCase(TestCase):
    databases = {'bart'}

    def setUp(self):
        # Set up data for the tests
        self.client = APIClient()
        self.test_agency = Agency.objects.create(agency_id="test_agency", agency_name="Test Agency Name")
        # self.url = reverse('agency-detail', kwargs={'agency_id': self.test_agency.agency_id})

    def test_get_agency_detail(self):
        # Test retrieving an agency by agency_id
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['agency_id'], self.test_agency.agency_id)
        self.assertEqual(response.data['agency_name'], self.test_agency.agency_name)

    def test_agency_not_found(self):
        # Test retrieving an agency that does not exist
        url = reverse('agency-detail', kwargs={'agency_id': 'nonexistent_agency'})
        response = self.client.get(url)
        self.assertEqual(response.status_status_code, status.HTTP_404_NOT_FOUND)

    def test_agency_list(self):
        response = self.client.get(reverse('agency-list'))
        self.assertEqual(response.status_code, 200)
        
        # Check if the response is JSON and decode it
        if response['Content-Type'] == 'application/json':
            response_data = response.json()
            # Assuming the response should be a list of agencies, check if any agency contains 'agency_id'
            self.assertTrue(any('agency_id' in agency for agency in response_data), "Response does not contain 'agency_id'")
        else:
            # If the response is not JSON, directly search for 'agency_id' in the response content
            self.assertContains(response, "agency_id")

class ServiceInfoTests(TestCase):
    def setup(self):
        self.alert = RealtimeAlert.objects.create(
            info = 'test info'
        )

        self.trip = Trip.objects.create(
            route_id = 1,
            service_id = '2024_08_12-DX-MVS-Weekday-01',
            trip_id = 1560937,
            trip_headsign = 'San Francisco International Airport',
            direction_id = 1,
            shape_id = '001A_shp'
        )

        self.stop = Stop.objects.create(
            stop_id = 'LAKE',
            stop_name = 'Lake Merrit',
            stop_lat = 37.7749,
            stop_lon = -122.4194,
            location_type = 0
        )

        self.stop_time_update = RealtimeStopTimeUpdate.objects.create(
            trip_id=self.trip,
            stop_id=self.stop,
            arrival_delay=0,
            arrival_time="0",
            arrival_uncertainty=0,
            departure_delay=0,
            departure_time="0",
            departure_uncertainty=0
        )

    def test_alert_info(self):
        response = self.client.get(reverse('alerts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "info")



# Test database integrity using fixture
class DatabaseTests(TestCase):
    databases = {'bart'}
    fixtures = ['bart_data.json']

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

    def test_realtime_stop_time_update_list(self):
        response = self.client.get(reverse('realtimestoptimeupdate-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "stop_id")

    def test_realtime_alert_list(self):
        response = self.client.get(reverse('realtimealert-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "alert_id")
        self.assertContains(response, "info")

    def test_realtime_trip_list(self):
        response = self.client.get(reverse('realtimetrip-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "trip_id")
        self.assertContains(response, "schedule_relationship")
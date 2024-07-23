import csv
import datetime
import os
import requests
import tempfile

import sqlite3
import zipfile

def get_gtfs_data():
    conn = sqlite3.connect('/workspaces/bartalysis/backend/bart.db')
    curr = conn.cursor()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_zip_path = temp_dir + '/temp.zip'
        url = 'https://www.bart.gov/dev/schedules/google_transit.zip'

        with requests.get(url, allow_redirects=True, stream=True) as r:
            r.raise_for_status()
            with open(temp_zip_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Agency
        with open(temp_dir + '/agency.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_agency = '''
            INSERT INTO agency (
                agency_id,
                agency_name,
                agency_url,
                agency_timezone,
                agency_phone
            )
            VALUES (?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_agency, (
                    empty_to_none(row['agency_id']),
                    empty_to_none(row['agency_name']),
                    empty_to_none(row['agency_url']),
                    empty_to_none(row['agency_timezone']),
                    empty_to_none(row['agency_phone'])
                ))

        # Feed Info
        with open(temp_dir + '/feed_info.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_feed_info = '''
            INSERT INTO feed_info (
                feed_publisher_name,
                feed_publisher_url,
                feed_lang,
                feed_start_date,
                feed_end_date,
                feed_version
            )
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_feed_info, (
                    empty_to_none(row['feed_publisher_name']),
                    empty_to_none(row['feed_publisher_url']),
                    empty_to_none(row['feed_lang']),
                    datetime.datetime.strptime(str(row['feed_start_date']), "%Y%m%d").strftime("%Y-%m-%d"),
                    datetime.datetime.strptime(str(row['feed_end_date']), "%Y%m%d").strftime("%Y-%m-%d"),
                    empty_to_none(row['feed_version'])
                ))

        # Fare Attributes
        with open(temp_dir + '/fare_attributes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_fare_attribute = '''
            INSERT INTO fare_attributes (
                fare_id,
                price,
                currency_type,
                payment_method
            )
            VALUES (?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_fare_attribute, (
                    empty_to_none(row['fare_id']),
                    empty_to_none(row['price']),
                    empty_to_none(row['currency_type']),
                    empty_to_none(row['payment_method'])
                ))

        # Fare Rules
        with open(temp_dir + '/fare_rules.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_fare_rule = '''
            INSERT INTO fare_rules (
                fare_id,
                origin_id,
                destination_id
            )
            VALUES (?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_fare_rule, (
                    empty_to_none(row['fare_id']),
                    empty_to_none(row['origin_id']),
                    empty_to_none(row['destination_id']),
                ))

        # Rider Categories
        with open(temp_dir + '/rider_categories.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_rider_category = '''
            INSERT INTO rider_categories (
            rider_category_id,
            rider_category_description
            )
            VALUES (?, ?)
            '''

            for row in reader:
                curr.execute(insert_rider_category, (
                    empty_to_none(row['rider_category_id']),
                    empty_to_none(row['rider_category_description'])
                ))

        # Fare Rider Categories
        with open(temp_dir + '/fare_rider_categories.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_fare_rider_category = '''
            INSERT INTO fare_rider_categories (
                fare_id,
                rider_category_id,
                price
            )
            VALUES (?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_fare_rider_category, (
                    empty_to_none(row['fare_id']),
                    empty_to_none(row['rider_category_id']),
                    empty_to_none(row['price'])
                ))

        # Shapes
        with open(temp_dir + '/shapes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_shape = '''
            INSERT INTO shapes (
                shape_id,
                shape_pt_lat,
                shape_pt_lon,
                shape_pt_sequence,
                shape_dist_traveled
            )
            VALUES (?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_shape, (
                    empty_to_none(row['shape_id']),
                    empty_to_none(row['shape_pt_lat']),
                    empty_to_none(row['shape_pt_lon']),
                    empty_to_none(row['shape_pt_sequence']),
                    empty_to_none(row['shape_dist_traveled'])
                ))

        # Routes
        with open(temp_dir + '/routes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_route = '''
            INSERT INTO routes (
                route_id,
                route_short_name,
                route_long_name,
                route_desc,
                route_type,
                route_url,
                route_color,
                route_text_color
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_route, (
                    empty_to_none(row['route_id']),
                    empty_to_none(row['route_short_name']),
                    empty_to_none(row['route_long_name']),
                    empty_to_none(row['route_desc']),
                    empty_to_none(row['route_type']),
                    empty_to_none(row['route_url']),
                    empty_to_none(row['route_color']),
                    empty_to_none(row['route_text_color'])
                ))

        # Route Attributes
        with open(temp_dir + '/route_attributes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_route_attribute = '''
            INSERT OR IGNORE INTO route_attributes (
                route_id,
                category,
                subcategory,
                running_way
            )
            VALUES (?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_route_attribute, (
                    empty_to_none(row['route_id']),
                    empty_to_none(row['category']),
                    empty_to_none(row['subcategory']),
                    empty_to_none(row['running_way'])
                ))

        # Realtime Routes
        with open(temp_dir + '/realtime_routes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_realtime_route = '''
            INSERT INTO realtime_routes (
                route_id,
                realtime_enabled
            )
            VALUES (?, ?)
            '''

            for row in reader:
                curr.execute(insert_realtime_route, (
                    empty_to_none(row['route_id']),
                    empty_to_none(row['realtime_enabled'])
                ))

        # Directions
        with open(temp_dir + '/directions.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_direction = '''
            INSERT INTO directions (
                route_id,
                direction_id,
                direction
            )
            VALUES (?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_direction, (
                    empty_to_none(row['route_id']),
                    empty_to_none(row['direction_id']),
                    empty_to_none(row['direction'])
                ))

        # Stops
        with open(temp_dir + '/stops.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_stop = '''
            INSERT INTO stops (
                stop_id,
                stop_name,
                stop_desc,
                stop_lat,
                stop_lon,
                zone_id,
                plc_url,
                location_type,
                parent_station
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_stop, (
                    empty_to_none(row['stop_id']),
                    empty_to_none(row['stop_name']),
                    empty_to_none(row['stop_desc']),
                    empty_to_none(row['stop_lat']),
                    empty_to_none(row['stop_lon']),
                    empty_to_none(row['zone_id']),
                    empty_to_none(row['plc_url']),
                    empty_to_none(row['location_type']),
                    empty_to_none(row['parent_station'])
                ))

        # Stop Times
        with open(temp_dir + '/stop_times.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_stop_time = '''
            INSERT INTO stop_times (
                trip_id,
                arrival_time,
                departure_time,
                stop_id,
                stop_sequence,
                stop_headsign,
                shape_distance_traveled
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_stop_time, (
                    empty_to_none(row['trip_id']),
                    empty_to_none(row['arrival_time']),
                    empty_to_none(row['departure_time']),
                    empty_to_none(row['stop_id']),
                    empty_to_none(row['stop_sequence']),
                    empty_to_none(row['stop_headsign']),
                    empty_to_none(row['shape_distance_traveled'])
                ))

        # Transfers
        with open(temp_dir + '/transfers.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_transfer = '''
            INSERT INTO transfers (
                from_stop_id,
                to_stop_id,
                transfer_type,
                min_transfer_time,
                from_route_id,
                to_route_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_transfer, (
                    empty_to_none(row['from_stop_id']),
                    empty_to_none(row['to_stop_id']),
                    empty_to_none(row['transfer_type']),
                    empty_to_none(row['min_transfer_time']),
                    empty_to_none(row['from_route_id']),
                    empty_to_none(row['to_route_id'])
                ))
        # Calendar
        with open(temp_dir + '/calendar.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_calendar = '''
            INSERT INTO calendar (
                service_id,
                monday,
                tuesday,
                wednesday,
                thursday,
                friday,
                saturday,
                sunday,
                start_date,
                end_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_calendar, (
                    empty_to_none(row['service_id']),
                    empty_to_none(row['monday']),
                    empty_to_none(row['tuesday']),
                    empty_to_none(row['wednesday']),
                    empty_to_none(row['thursday']),
                    empty_to_none(row['friday']),
                    empty_to_none(row['saturday']),
                    empty_to_none(row['sunday']),
                    datetime.datetime.strptime(str(row['start_date']), "%Y%m%d").strftime("%Y-%m-%d"),
                    datetime.datetime.strptime(str(row['end_date']), "%Y%m%d").strftime("%Y-%m-%d")
                ))

        # Calendar Attributes
        with open(temp_dir + '/calendar_attributes.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_calendar_attribute = '''
            INSERT INTO calendar_attributes (
                service_id,
                service_description
            )
            VALUES (?, ?)
            '''

            for row in reader:
                curr.execute(insert_calendar_attribute, (
                    empty_to_none(row['service_id']),
                    empty_to_none(row['service_description'])
                ))

        # Calendar Dates
        with open(temp_dir + '/calendar_dates.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_calendar_date = '''
            INSERT INTO calendar_dates (
                service_id,
                date,
                exception_type
            )
            VALUES (?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_calendar_date, (
                    empty_to_none(row['service_id']),
                    datetime.datetime.strptime(str(row['date']), "%Y%m%d").strftime("%Y-%m-%d"),
                    empty_to_none(row['exception_type'])
                ))

        # Trips
        with open(temp_dir + '/trips.txt', 'r') as csvfile:
            reader = csv.DictReader(csvfile)

            insert_trip = '''
            INSERT INTO trips (
                route_id,
                service_id,
                trip_id,
                trip_headsign,
                direction_id,
                shape_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            '''

            for row in reader:
                curr.execute(insert_trip, (
                    empty_to_none(row['route_id']),
                    empty_to_none(row['service_id']),
                    empty_to_none(row['trip_id']),
                    empty_to_none(row['trip_headsign']),
                    empty_to_none(row['direction_id']),
                    empty_to_none(row['shape_id'])
                ))

    conn.commit()
    conn.close()

def empty_to_none(value):
    return None if value == "" else value

get_gtfs_data()

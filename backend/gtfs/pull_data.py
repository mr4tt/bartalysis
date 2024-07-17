import csv
import datetime
import os
import requests
import sqlite3
import zipfile

def get_gtfs_data():
    temp_zip_path = "temp.zip"
    url = "https://www.bart.gov/dev/schedules/google_transit.zip"
    path = "/workspaces/bartalysis/backend/gtfs/data/"

    with requests.get(url, allow_redirects=True, stream=True) as r:
        r.raise_for_status()
        with open(temp_zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
        zip_ref.extractall(path)

    os.remove(temp_zip_path)

def write_gtfs_data():
    get_gtfs_data()

    conn = sqlite3.connect('/workspaces/bartalysis/backend/bart.db')
    curr = conn.cursor()
    path = "/workspaces/bartalysis/backend/gtfs/data/"

    # Agency
    with open(path + '/agency.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_agency = '''
        INSERT INTO agency (
            agency_id,
            agency_name,
            agency_url,
            agency_timezone,
            agency_lang,
            agency_phone
        )
        VALUES (?, ?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_agency, (
                empty_to_none(row['agency_id']),
                empty_to_none(row['agency_name']),
                empty_to_none(row['agency_url']),
                empty_to_none(row['agency_timezone']),
                empty_to_none(row['agency_lang']),
                empty_to_none(row['agency_phone'])
            ))
        os.remove(path + '/agency.txt')

    # Feed Info
    with open(path + '/feed_info.txt', 'r') as csvfile:
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
                datetime.datetime.strptime(str(row['feed_start_date']), "%Y%m%d").strftime("%Y-%m-%d"),
                empty_to_none(row['feed_version'])
            ))
        os.remove(path + '/feed_info.txt')

    # Fare Attributes
    with open(path + '/fare_attributes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_fare_attribute = '''
        INSERT INTO fare_attributes (
            fare_id,
            price,
            currency_type,
            payment_method,
            transfers,
            transfer_duration
        )
        VALUES (?, ?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_fare_attribute, (
                empty_to_none(row['fare_id']),
                empty_to_none(row['price']),
                empty_to_none(row['currency_type']),
                empty_to_none(row['payment_method']),
                empty_to_none(row['transfers']),
                empty_to_none(row['transfer_duration'])
            ))
        os.remove(path + '/fare_attributes.txt')

    # Fare Rules
    with open(path + '/fare_rules.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_fare_rule = '''
        INSERT INTO fare_rules (
            fare_id,
            route_id,
            origin_id,
            destination_id,
            contains_id
        )
        VALUES (?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_fare_rule, (
                empty_to_none(row['fare_id']),
                empty_to_none(row['route_id']),
                empty_to_none(row['origin_id']),
                empty_to_none(row['destination_id']),
                empty_to_none(row['contains_id'])
            ))
        os.remove(path + '/fare_rules.txt')

    # Rider Categories
    with open(path + '/rider_categories.txt', 'r') as csvfile:
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
        os.remove(path + '/rider_categories.txt')

    # Fare Rider Categories
    with open(path + '/fare_rider_categories.txt', 'r') as csvfile:
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
        os.remove(path + '/fare_rider_categories.txt')

    # Shapes
    with open(path + '/shapes.txt', 'r') as csvfile:
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
        os.remove(path + '/shapes.txt')

    # Routes
    with open(path + '/routes.txt', 'r') as csvfile:
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
        os.remove(path + '/routes.txt')

    # Route Attributes
    with open(path + '/route_attributes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_route_attribute = '''
        INSERT INTO route_attributes (
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
        os.remove(path + '/route_attributes.txt')

    # Realtime Routes
    with open(path + '/realtime_routes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_realtime_route = '''
        INSERT INTO realtime_routes (
            route_id,
            realtime_enabled,
            realtime_routename,
            realtime_routecode
        )
        VALUES (?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_realtime_route, (
                empty_to_none(row['route_id']),
                empty_to_none(row['realtime_enabled']),
                empty_to_none(row['realtime_routename']),
                empty_to_none(row['realtime_routecode'])
            ))
        os.remove(path + '/realtime_routes.txt')

    # Directions
    with open(path + '/directions.txt', 'r') as csvfile:
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
        os.remove(path + '/directions.txt')

    # Stops
    with open(path + '/stops.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_stop = '''
        INSERT INTO stops (
            stop_id,
            stop_code,
            stop_name,
            stop_desc,
            stop_lat,
            stop_lon,
            zone_id,
            plc_url,
            location_type,
            parent_station
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_stop, (
                empty_to_none(row['stop_id']),
                empty_to_none(row['stop_code']),
                empty_to_none(row['stop_name']),
                empty_to_none(row['stop_desc']),
                empty_to_none(row['stop_lat']),
                empty_to_none(row['stop_lon']),
                empty_to_none(row['zone_id']),
                empty_to_none(row['plc_url']),
                empty_to_none(row['location_type']),
                empty_to_none(row['parent_station'])
            ))
        os.remove(path + '/stops.txt')

    # Stop Times
    with open(path + '/stop_times.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_stop_time = '''
        INSERT INTO stop_times (
            trip_id,
            arrival_time,
            departure_time,
            stop_id,
            stop_sequence,
            stop_headsign,
            pickup_type,
            drop_off_type,
            shape_distance_traveled
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_stop_time, (
                empty_to_none(row['trip_id']),
                empty_to_none(row['arrival_time']),
                empty_to_none(row['departure_time']),
                empty_to_none(row['stop_id']),
                empty_to_none(row['stop_sequence']),
                empty_to_none(row['stop_headsign']),
                empty_to_none(row['pickup_type']),
                empty_to_none(row['drop_off_type']),
                empty_to_none(row['shape_distance_traveled'])
            ))
        os.remove(path + '/stop_times.txt')

    # Transfers
    with open(path + '/transfers.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_transfer = '''
        INSERT INTO transfers (
            from_stop_id,
            to_stop_id,
            transfer_type,
            min_transfer_time
        )
        VALUES (?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_transfer, (
                empty_to_none(row['from_stop_id']),
                empty_to_none(row['to_stop_id']),
                empty_to_none(row['transfer_type']),
                empty_to_none(row['min_transfer_time'])
            ))
        os.remove(path + '/transfers.txt')

    # Calendar
    with open(path + '/calendar.txt', 'r') as csvfile:
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
        os.remove(path + '/calendar.txt')

    # Calendar Attributes
    with open(path + '/calendar_attributes.txt', 'r') as csvfile:
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
        os.remove(path + '/calendar_attributes.txt')

    # Calendar Dates
    with open(path + '/calendar_dates.txt', 'r') as csvfile:
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
        os.remove(path + '/calendar_dates.txt')

    # Trips
    with open(path + '/trips.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_trip = '''
        INSERT INTO trips (
            route_id,
            service_id,
            trip_id,
            trip_headsign,
            direction_id,
            block_id,
            shape_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_trip, (
                empty_to_none(row['route_id']),
                empty_to_none(row['service_id']),
                empty_to_none(row['trip_id']),
                empty_to_none(row['trip_headsign']),
                empty_to_none(row['direction_id']),
                empty_to_none(row['block_id']),
                empty_to_none(row['shape_id'])
            ))
        os.remove(path + '/trips.txt')

    conn.commit()
    conn.close()

    os.rmdir(path)

def empty_to_none(value):
    return None if value == "" else value

write_gtfs_data()

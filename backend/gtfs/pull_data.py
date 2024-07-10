import requests
import zipfile
import os
import sqlite3
import csv

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

    #Agency
    with open(path + '/agency.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_agency = '''
        INSERT OR IGNORE INTO agency (
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
                row['agency_id'], 
                row['agency_name'], 
                row['agency_url'], 
                row['agency_timezone'], 
                row['agency_lang'], 
                row['agency_phone']
                ))
        os.remove(path + '/agency.txt')
    
    #Feed Info
    with open(path + '/feed_info.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_feed_info = '''
        INSERT OR IGNORE INTO feed_info (
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
                row['feed_publisher_name'],
                row['feed_publisher_url'],
                row['feed_lang'],
                row['feed_start_date'],
                row['feed_end_date'],
                row['feed_version']
                ))
        os.remove(path + '/feed_info.txt')

    #Calendar
    with open(path + '/calendar.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_calendar = '''
        INSERT OR IGNORE INTO calendar (
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
                row['service_id'],
                row['monday'],
                row['tuesday'],
                row['wednesday'],
                row['thursday'],
                row['friday'],
                row['saturday'],
                row['sunday'],
                row['start_date'],
                row['end_date']
                ))
        os.remove(path + '/calendar.txt')
    
    #Calendar Attributes
    with open(path + '/calendar_attributes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_calendar_attribute = '''
        INSERT OR IGNORE INTO calendar_attribute (
            service_id,
            service_description
        )
        VALUES (?, ?)
        '''

        for row in reader:
            curr.execute(insert_calendar_attribute, (
                row['service_id'],
                row['service_description']
                ))
        os.remove(path + '/calendar_attributes.txt')

    #Calendar Dates
    with open(path + '/calendar_dates.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_calendar_date = '''
        INSERT OR IGNORE INTO calendar_date (
            service_id,
            date,
            exception_type
        )
        VALUES (?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_calendar_date, (
                row['service_id'],
                row['date'],
                row['exception_type']
                ))
        os.remove(path + '/calendar_dates.txt')
    
    #Fare Attributes
    with open(path + '/fare_attributes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_fare_attribute = '''
        INSERT OR IGNORE INTO fare_attribute (
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
                row['fare_id'],
                row['price'],
                row['currency_type'],
                row['payment_method'],
                row['transfers'],
                row['transfer_duration']
                ))
        os.remove(path + '/fare_attributes.txt')

    #Fare Rider Categories
    with open(path + '/fare_rider_categories.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_fare_rider_category = '''
        INSERT OR IGNORE INTO fare_rider_category (
            fare_id,
            rider_category_id,
            price
        )
        VALUES (?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_fare_rider_category, (
                row['fare_id'],
                row['rider_category_id'],
                row['price']
                ))
        os.remove(path + '/fare_rider_categories.txt')
    
    #Fare Rules
    with open(path + '/fare_rules.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_fare_rule = '''
        INSERT OR IGNORE INTO fare_rule (
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
                row['fare_id'],
                row['route_id'],
                row['origin_id'],
                row['destination_id'],
                row['contains_id']
                ))
        os.remove(path + '/fare_rules.txt')
    
    #Routes
    with open(path + '/routes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_route = '''
        INSERT OR IGNORE INTO route (
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
                row['route_id'],
                row['route_short_name'],
                row['route_long_name'],
                row['route_desc'],
                row['route_type'],
                row['route_url'],
                row['route_color'],
                row['route_text_color']
                ))
        os.remove(path + '/routes.txt')
    
    #Route Attributes
    with open(path + '/route_attributes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_route_attribute = '''
        INSERT OR IGNORE INTO route_attribute (
            route_id,
            category,
            subcategory,
            running_way
        )
        VALUES (?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_route_attribute, (
                row['route_id'],
                row['category'],
                row['subcategory'],
                row['running_way']
                ))
        os.remove(path + '/route_attributes.txt')

    #Directions
    with open(path + '/directions.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_direction = '''
        INSERT OR IGNORE INTO direction (
            route_id,
            direction_id,
            direction
        )
        VALUES (?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_direction, (
                row['route_id'],
                row['direction_id'],
                row['direction']
                ))
        os.remove(path + '/directions.txt')
    
    #Realtime Routes
    with open(path + '/realtime_routes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_realtime_route = '''
        INSERT OR IGNORE INTO realtime_route (
            route_id,
            realtime_enabled,
            realtime_routename,
            realtime_routecode
        )
        VALUES (?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_realtime_route, (
                row['route_id'],
                row['realtime_enabled'],
                row['realtime_routename'],
                row['realtime_routecode']
                ))
        os.remove(path + '/realtime_routes.txt')
    
    #Rider Categories
    with open(path + '/rider_categories.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_rider_category = '''
        INSERT OR IGNORE INTO rider_category (
        rider_category_id,
        rider_category_description
        )
        VALUES (?, ?)
        '''

        for row in reader:
            curr.execute(insert_rider_category, (
                row['rider_category_id'],
                row['rider_category_description']
                ))
        os.remove(path + '/rider_categories.txt')

    #Shapes
    with open(path + '/shapes.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_shape = '''
        INSERT OR IGNORE INTO shape (
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
                row['shape_id'],
                row['shape_pt_lat'],
                row['shape_pt_lon'],
                row['shape_pt_sequence'],
                row['shape_dist_traveled']
                ))
        os.remove(path + '/shapes.txt')

    #Trips
    with open(path + '/trips.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_trip = '''
        INSERT OR IGNORE INTO trip (
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
                row['route_id'],
                row['service_id'],
                row['trip_id'],
                row['trip_headsign'],
                row['direction_id'],
                row['block_id'],
                row['shape_id']
                ))
        os.remove(path + '/trips.txt')
    
    #Stops
    with open(path + '/stops.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_stop = '''
        INSERT OR IGNORE INTO stop (
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
                row['stop_id'],
                row['stop_code'],
                row['stop_name'],
                row['stop_desc'],
                row['stop_lat'],
                row['stop_lon'],
                row['zone_id'],
                row['plc_url'],
                row['location_type'],
                row['parent_station']
                ))
        os.remove(path + '/stops.txt')
    
    #Stop Times
    with open(path + '/stop_times.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_stop_time = '''
        INSERT OR IGNORE INTO stop_time (
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
                row['trip_id'],
                row['arrival_time'],
                row['departure_time'],
                row['stop_id'],
                row['stop_sequence'],
                row['stop_headsign'],
                row['pickup_type'],
                row['drop_off_type'],
                row['shape_distance_traveled']
                ))
        os.remove(path + '/stop_times.txt') 
    
    #Transfers
    with open(path + '/transfers.txt', 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        insert_transfer = '''
        INSERT OR IGNORE INTO transfer (
            from_stop_id,
            to_stop_id,
            transfer_type,
            min_transfer_time
        )
        VALUES (?, ?, ?, ?)
        '''

        for row in reader:
            curr.execute(insert_transfer, (
                row['from_stop_id'],
                row['to_stop_id'],
                row['transfer_type'],
                row['min_transfer_time']
                ))
        os.remove(path + '/transfers.txt')

    conn.commit()
    conn.close()

    os.rmdir(path)

write_gtfs_data()
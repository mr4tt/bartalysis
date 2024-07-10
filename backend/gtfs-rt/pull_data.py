import datetime
from datetime import datetime, timezone

import requests
import re
import sqlite3
import gtfs_realtime_pb2

def get_alerts():
    url = "http://api.bart.gov/gtfsrt/alerts.aspx"
    feed = gtfs_realtime_pb2.FeedMessage()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        feed.ParseFromString(r.content)

    conn = sqlite3.connect('/workspaces/bartalysis/backend/bart.db')
    curr = conn.cursor()

    insert_alert = '''
    INSERT OR IGNORE INTO rt_alert (
    alert_id,
    info, 
    lang
    )
    VALUES (?, ?, ?)
    '''

    for entity in feed.entity:
        if entity.HasField('alert'):
            alert_id = re.sub(r'\D', '', entity.id)
            info = entity.alert.description_text.translation[0].text
            lang = entity.alert.description_text.translation[1].text if len(entity.alert.description_text.translation) > 1 else "en-US"
            
            # Execute the INSERT statement with the extracted values
            curr.execute(insert_alert, (
                alert_id, 
                info, 
                lang
                ))
    conn.commit()
    conn.close()

def get_trip_updates():
    url = "http://api.bart.gov/gtfsrt/tripupdate.aspx"
    feed = gtfs_realtime_pb2.FeedMessage()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        feed.ParseFromString(r.content)

    conn = sqlite3.connect('/workspaces/bartalysis/backend/bart.db')
    curr = conn.cursor()

    insert_trip = '''
    INSERT OR IGNORE INTO rt_trip (
    trip_id,
    schedule_relationship, 
    vehicle
    ) 
    VALUES (?, ?, ?)
    '''

    insert_stop_time = '''
    INSERT OR IGNORE INTO rt_stop_time_update (
    trip_id, 
    stop_id, 
    arrival_delay, 
    arrival_time, 
    arrival_uncertainty, 
    departure_delay, 
    departure_time, 
    departure_uncertainty
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_id = entity.trip_update.trip.trip_id
            schedule_relationship = entity.trip_update.trip.schedule_relationship
            vehicle_label = entity.trip_update.vehicle.label
            curr.execute(insert_trip, (
                trip_id,
                schedule_relationship,
                vehicle_label
            ))

            for stop_time_update in entity.trip_update.stop_time_update:
                stop_id = stop_time_update.stop_id
                arrival_delay = stop_time_update.arrival.delay
                arrival_time = datetime.fromtimestamp(stop_time_update.arrival.time, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                arrival_uncertainty = stop_time_update.arrival.uncertainty
                departure_delay = stop_time_update.departure.delay
                departure_time = datetime.fromtimestamp(stop_time_update.departure.time, tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
                departure_uncertainty = stop_time_update.departure.uncertainty
                curr.execute(insert_stop_time, (
                    trip_id,
                    stop_id,
                    arrival_delay,
                    arrival_time,
                    arrival_uncertainty,
                    departure_delay,
                    departure_time,
                    departure_uncertainty
                ))

    conn.commit()
    conn.close()
                    
get_trip_updates()
get_alerts()
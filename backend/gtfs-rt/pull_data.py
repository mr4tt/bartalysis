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
    INSERT INTO realtime_alerts (
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
    INSERT INTO realtime_trips (
    trip_id,
    schedule_relationship, 
    vehicle
    ) 
    VALUES (?, ?, ?)
    '''

    insert_stop_time = '''
    INSERT INTO realtime_stop_time_updates (
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
                arrival_time = stop_time_update.arrival.time
                arrival_uncertainty = stop_time_update.arrival.uncertainty
                departure_delay = stop_time_update.departure.delay
                departure_time = stop_time_update.departure.time
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
import requests
import gtfs_realtime_pb2

def get_trip_updates():
    url = "http://api.bart.gov/gtfsrt/tripupdate.aspx"
    feed = gtfs_realtime_pb2.FeedMessage()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        feed.ParseFromString(r.content)

    with open('trip_updates.txt', 'w') as result_file:
        for entity in feed.entity:
            print(entity.trip_update.stop_time_update)
            result_file.write(str(entity) + '\n')
                
def get_alerts():
    url = "http://api.bart.gov/gtfsrt/alerts.aspx"
    feed = gtfs_realtime_pb2.FeedMessage()

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        feed.ParseFromString(r.content)

    with open('alerts.txt', 'w') as result_file:
        for entity in feed.entity:
            result_file.write(str(entity) + '\n')
get_trip_updates()
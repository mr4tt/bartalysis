import heapq
from .models import Stop, StopTime, Trip, RealtimeStopTimeUpdate

def build_graph():
    graph = {}
    stop_times = StopTime.objects.all()
    for stop_time in stop_times:
        trip_id = stop_time.trip_id.trip_id
        stop_id = stop_time.stop_id.stop_id
        arrival_time = stop_time.arrival_time
        departure_time = stop_time.departure_time
        if trip_id not in graph:
            graph[trip_id] = []
        graph[trip_id].append((stop_id, arrival_time, departure_time))
    return graph

def update_with_realtime(graph):
    realtime_updates = RealtimeStopTimeUpdate.objects.all()
    for update in realtime_updates:
        trip_id = update.trip_id.trip_id
        stop_id = update.stop_id.stop_id
        arrival_delay = update.arrival_delay
        departure_delay = update.departure_delay
        if trip_id in graph:
            for i, (stop, arrival, departure) in enumerate(graph[trip_id]):
                if stop == stop_id:
                    graph[trip_id][i] = (stop, arrival + arrival_delay, departure + departure_delay)
    return graph

def dijkstra(graph, start, end):
    queue = [(0, start)]
    distances = {stop: float('infinity') for stop in graph}
    distances[start] = 0
    shortest_path = {}
    while queue:
        (current_distance, current_stop) = heapq.heappop(queue)
        if current_distance > distances[current_stop]:
            continue
        for neighbor, arrival_time, departure_time in graph[current_stop]:
            distance = current_distance + (departure_time - arrival_time)
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                shortest_path[neighbor] = current_stop
                heapq.heappush(queue, (distance, neighbor))
    path = []
    stop = end
    while stop != start:
        path.append(stop)
        stop = shortest_path[stop]
    path.append(start)
    path.reverse()
    return path, distances[end]

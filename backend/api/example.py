import sqlite3

# Returns list of station names
def get_station_names():
    conn = sqlite3.connect('/workspaces/bartalysis/backend/bart.db')
    curr = conn.cursor()

    query = '''
    SELECT stop_name FROM stop
    WHERE location_type = 0
    '''

    curr.execute(query)
    stations = curr.fetchall()
    conn.close()

    return stations
print(get_station_names())
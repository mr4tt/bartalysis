DROP TABLE IF EXISTS agency;
CREATE TABLE agency (
    agency_id TEXT PRIMARY KEY,
    agency_name TEXT NOT NULL,
    agency_url TEXT NOT NULL,
    agency_timezone TEXT,
    agency_lang TEXT,
    agency_phone TEXT NOT NULL
);

DROP TABLE IF EXISTS feed_info;
CREATE TABLE feed_info (
    feed_publisher_name TEXT NOT NULL,
    feed_publisher_url TEXT NOT NULL,
    feed_lang TEXT NOT NULL,
    feed_start_date INT NOT NULL,
    feed_end_date INT NOT NULL,
    feed_version TEXT NOT NULL
);

DROP TABLE IF EXISTS calendar;
CREATE TABLE calendar (
    service_id TEXT PRIMARY KEY,
    monday INT NOT NULL,
    tuesday INT NOT NULL,
    wednesday INT NOT NULL,
    thursday INT NOT NULL,
    friday INT NOT NULL,
    saturday INT NOT NULL,
    sunday INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL
);

DROP TABLE IF EXISTS calendar_attribute;
CREATE TABLE calendar_attribute (
    service_id TEXT PRIMARY KEY REFERENCES calendar(service_id),
    service_description TEXT NOT NULL
);
w
DROP TABLE IF EXISTS calendar_date;
CREATE TABLE calendar_date (
    service_id TEXT REFERENCES calendar(service_id),
    date DATE NOT NULL,
    exception_type INT NOT NULL
);

DROP TABLE IF EXISTS fare_attribute;
CREATE TABLE fare_attribute (
    fare_id INT PRIMARY KEY,
    price INT NOT NULL,
    currency_type TEXT NOT NULL,
    payment_method INT NOT NULL,
    transfers INT,
    transfer_duration INT
);

DROP TABLE IF EXISTS fare_rider_category;
CREATE TABLE fare_rider_category (
    fare_id INT REFERENCES fare_attribute(fare_id),
    rider_category_id INT NOT NULL,
    price INT NOT NULL
);

DROP TABLE IF EXISTS fare_rule;
CREATE TABLE fare_rule (
    fare_id INT REFERENCES fare_attribute(fare_id),
    route_id TEXT,
    origin_id TEXT NOT NULL,
    destination_id TEXT NOT NULL,
    contains_id TEXT
);

DROP TABLE IF EXISTS route;
CREATE TABLE route (
    route_id TEXT PRIMARY KEY,
    route_short_name TEXT NOT NULL,
    route_long_name TEXT,
    route_desc TEXT NOT NULL,
    route_type INT NOT NULL,
    route_url TEXT,
    route_color TEXT NOT NULL,
    route_text_color TEXT NOT NULL
);

DROP TABLE IF EXISTS route_attribute;
CREATE TABLE route_attribute (
    route_id TEXT REFERENCES route(route_id),
    category TEXT NOT NULL,
    subcategory TEXT NOT NULL,
    running_way TEXT NOT NULL
);

DROP TABLE IF EXISTS direction;
CREATE TABLE direction (
    route_id TEXT PRIMARY KEY,
    direction_id TEXT NOT NULL,
    direction TEXT NOT NULL
);

DROP TABLE IF EXISTS realtime_route;
CREATE TABLE realtime_route (
    route_id TEXT PRIMARY KEY,
    realtime_enabled BOOLEAN NOT NULL,
    realtime_routename TEXT,
    realtime_routecode TEXT
);

DROP TABLE IF EXISTS rider_category;
CREATE TABLE rider_category (
    rider_category_id INT PRIMARY KEY,
    rider_category_description TEXT NOT NULL
);

DROP TABLE IF EXISTS shape;
CREATE TABLE shape (
    shape_id TEXT PRIMARY KEY,
    shape_pt_lat INT NOT NULL,
    shape_pt_lon INT NOT NULL,
    shape_pt_sequence INT NOT NULL,
    shape_dist_traveled INT NOT NULL
);

DROP TABLE IF EXISTS trip;
CREATE TABLE trip (
    route_id TEXT REFERENCES route(route_id),
    service_id TEXT REFERENCES calendar_attribute(service_id),
    trip_id INT PRIMARY KEY,
    trip_headsign TEXT NOT NULL,
    direction_id TEXT NOT NULL,
    block_id TEXT NOT NULL,
    shape_id TEXT NOT NULL
);  

DROP TABLE IF EXISTS stop;
CREATE TABLE stop (
    stop_id TEXT PRIMARY KEY,
    stop_code TEXT NOT NULL,
    stop_name TEXT NOT NULL,
    stop_desc TEXT NOT NULL,
    stop_lat TEXT NOT NULL,
    stop_lon TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    plc_url TEXT NOT NULL,
    location_type INT NOT NULL,
    parent_station TEXT NOT NULL
);

DROP TABLE IF EXISTS stop_time;
CREATE TABLE stop_time (
    trip_id INT PRIMARY KEY,
    arrival_time TIME NOT NULL,
    departure_time TIME NOT NULL,
    stop_id TEXT REFERENCES stop(stop_id),
    stop_sequence TEXT,
    stop_headsign TEXT,
    pickup_type INT,
    drop_off_type INT,
    shape_distance_traveled INT NOT NULL
);

DROP TABLE IF EXISTS transfer;
CREATE TABLE transfer (
    from_stop_id TEXT NOT NULL,
    to_stop_id TEXT NOT NULL,
    transfer_type INT NOT NULL,
    min_transfer_time INT NOT NULL
);

DROP TABLE IF EXISTS rt_alert;
CREATE TABLE rt_alert (
    id INT PRIMARY KEY,
    info TEXT NOT NULL,
    lang TEXT NOT NULL
);

DROP TABLE IF EXISTS rt_trip;
CREATE TABLE rt_trip (
    id INT PRIMARY KEY,
    schedule_relationship TEXT NOT NULL,
    vehicle TEXT NOT NULL
);

DROP TABLE IF EXISTS rt_stop_time_update;
CREATE TABLE rt_stop_time_update (
    id INT PRIMARY KEY,
    trip_id INT REFERENCES trip(trip_id), 
    stop_id TEXT NOT NULL,
    arrival_delay INT NOT NULL,
    arrival_time DATETIME NOT NULL,
    arrival_uncertainty INT NOT NULL,
    departure_delay INT NOT NULL,
    departure_time DATETIME NOT NULL,
    departure_uncertainty INT NOT NULL
);
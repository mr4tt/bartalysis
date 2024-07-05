DROP TABLE IF EXISTS alert;
CREATE TABLE alert (
    id INT PRIMARY KEY,
    info TEXT NOT NULL,
    lang TEXT NOT NULL
);

DROP TABLE IF EXISTS trip ;
CREATE TABLE trip (
    id INT PRIMARY KEY,
    schedule_relationship TEXT NOT NULL,
    vehicle TEXT NOT NULL
);

DROP TABLE IF EXISTS stop_time_update ;
CREATE TABLE stop_time_update (
    id INT PRIMARY KEY,
    trip_id INT REFERENCES trip(id), 
    stop_id TEXT NOT NULL,
    arrival_delay INT NOT NULL,
    arrival_time INT NOT NULL,
    arrival_uncertainty INT NOT NULL,
    departure_delay INT NOT NULL,
    departure_time INT NOT NULL,
    departure_uncertainty INT NOT NULL
);
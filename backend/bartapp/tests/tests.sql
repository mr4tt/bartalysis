/*
Input: <from station>, <end station>, <datetime>
Output: <first three trains>
Misc: <line>

Ex:
Input: SHAY, FRMT, 08:00:00


from station > stops.stop_id > stop_times.stop_id > trips.trip_id
==
trips.trip_id < stop_times.stop_id < stops.stop_id < end station

departure_time - time = time_difference > 0

shay.stop_times.stop_sqeunce < frmt.stop_times.stop_sequence
*/

-- .output result.txt
-- SELECT r.route_short_name, t.trip_id, t.trip_headsign, t.direction_id, t.route_id, st.arrival_time, st.departure_time, ca.service_description,
--     ABS(strftime('%s', st.departure_time) - strftime('%s', '08:00:00')) AS time_difference
-- FROM trips t
--     JOIN stop_times st ON t.trip_id = st.trip_id
--     JOIN stops s ON st.stop_id = s.stop_id
--     JOIN routes r ON t.route_id = r.route_id
--     JOIN calendar c ON t.service_id = c.service_id
--     JOIN calendar_attributes ca ON c.service_id = ca.service_id
-- WHERE s.stop_id = 'SHAY'
--     AND strftime('%s', st.departure_time) >= strftime('%s', '08:00:00')
--     AND c.thursday = 1
--     AND t.trip_id IN (
--         SELECT trip_id
--         FROM stop_times
--         WHERE stop_id IN (
--             SELECT stop_id
--             FROM stops
--             WHERE stop_id = 'FRMT'
--         )
--     )
    
-- ORDER BY time_difference
-- ;
-- .output stdout


--End of instruction example


-- Query producting the incoming trains information based on the following criteria:
-- origin station, destination station, date, time
-- Times are currently set to be PST in the settings.py file as that is where the BART system is located
-- All times are in the 24-hour format and are relative to PST
.output result1.txt
SELECT DISTINCT
    r.route_short_name AS TrainName, 
    r.route_color AS TrainColor, 
    r.route_long_name AS TrainDescription,
    st1.stop_id AS StartingID, 
    st2.stop_id AS EndingID, 
    st1.departure_time AS DepartureTime, 
    st2.arrival_time AS ArrivalTime
FROM trips t
JOIN stop_times st1 ON t.trip_id = st1.trip_id AND st1.stop_id = 'MCAR'
JOIN stop_times st2 ON t.trip_id = st2.trip_id AND st2.stop_id = 'FRMT'
JOIN routes r ON t.route_id = r.route_id
JOIN calendar c ON t.service_id = c.service_id
WHERE c.wednesday = 1
AND st1.departure_time > '08:00:00'
AND st1.stop_sequence < st2.stop_sequence
AND '2024-07-31' BETWEEN c.start_date AND c.end_date
ORDER BY st1.departure_time;
.output stdout


-- Query producing the fare information based on the following criteria:
-- origin station, destination station
.output result2.txt
SELECT DISTINCT FareID, Price, Description
FROM (
    -- Include regular prices with a default description
    SELECT
        fa.fare_id AS FareID,
        fa.price AS Price,
        'Regular' AS Description -- Default description for regular prices
    FROM fare_attributes fa
    WHERE fa.fare_id IN (
        SELECT fare_id FROM fare_rules
        WHERE origin_id = 'ANTC'
        AND destination_id = 'FRMT'
    )

    UNION ALL

    -- Include discounted prices
    SELECT
        frc.fare_id AS FareID,
        frc.price AS Price,
        rc.rider_category_description AS Description
    FROM fare_rider_categories frc
    JOIN rider_categories rc ON frc.rider_category_id = rc.rider_category_id
    WHERE frc.fare_id IN (
        SELECT fare_id FROM fare_rules
        WHERE origin_id = 'SHAY'
        AND destination_id = 'FRMT'
    )
) ORDER BY FareID, Description;
.output stdout


-- -- Queries producing service information based on realtime and static data for comparison.

-- -- Realtime mass data
-- .output result3.txt
-- SELECT
--     datetime(departure_time - (8 * 3600), 'unixepoch') AS readable_departure_time,
--     stop_id,
--     trip_id
-- FROM realtime_stop_time_updates
-- WHERE stop_id = 'SHAY'
-- ORDER BY departure_time;
-- .output stdout

-- .output result4.txt
-- SELECT 
--     st.stop_id,
--     st.stop_sequence,
--     st.departure_time,
--     st.trip_id,
--     r.route_short_name
-- FROM stop_times st
-- JOIN trips t ON st.trip_id = t.trip_id
-- JOIN routes r ON t.route_id = r.route_id
-- WHERE st.stop_id = 'SHAY'
-- AND departure_time > '10:45:00'
-- AND departure_time < '12:00:00'
-- ORDER BY r.route_short_name, st.departure_time;
-- .output stdout

-- -- Realtime data query for comparison
-- .output result5.txt
-- SELECT 
--     rstu.stop_id,
--     rstu.trip_id,
--     datetime(rstu.departure_time - (8 * 3600), 'unixepoch') AS readable_departure_time,
--     r.route_short_name
-- FROM realtime_stop_time_updates rstu
-- JOIN trips t ON rstu.trip_id = t.trip_id
-- JOIN routes r ON t.route_id = r.route_id
-- WHERE rstu.stop_id = 'SHAY'
-- ORDER BY r.route_short_name, rstu.departure_time;
-- .output stdout

-- -- Static data query for comparison
-- .output result6.txt
-- SELECT DISTINCT
--     st.stop_id,
--     st.departure_time,
--     r.route_short_name
-- FROM (
--     SELECT DISTINCT st.departure_time, r.route_short_name
--     FROM stop_times st
--     JOIN trips t ON st.trip_id = t.trip_id
--     JOIN routes r ON t.route_id = r.route_id
--     WHERE st.stop_id = 'SHAY'
--     AND st.departure_time > '10:48:00'
--     AND st.departure_time < '12:00:00'
-- ) dt
-- JOIN stop_times st ON st.departure_time = dt.departure_time
-- JOIN trips t ON st.trip_id = t.trip_id
-- JOIN routes r ON t.route_id = r.route_id
-- WHERE st.stop_id = 'SHAY'
-- ORDER BY r.route_short_name, st.departure_time;
-- .output stdout

.output result7.txt
SELECT DISTINCT
        st1.stop_id AS StartingID, 
        st2.stop_id AS TransferID,
        st2.departure_time AS TransferTime
    FROM trips t
    JOIN stop_times st1 ON t.trip_id = st1.trip_id AND st1.stop_id = 'ANTC'
    JOIN stop_times st2 ON t.trip_id = st2.trip_id
    JOIN routes r ON t.route_id = r.route_id
    JOIN calendar c ON t.service_id = c.service_id
    WHERE c.wednesday = 1
    AND st1.departure_time > '08:00:00'
    AND st1.stop_sequence < st2.stop_sequence
    AND '2024-07-31' BETWEEN c.start_date AND c.end_date
    ORDER BY st1.departure_time;
.output stdout


-- .output result8.txt
-- SELECT
--     to_stop_id,
--     from_route_id,
--     to_route_id
--     FROM transfers
--     WHERE from_route_id = 1;
-- .output stdout

.output result8.txt
SELECT DISTINCT
    s.stop_id,
    t.route_id,
    r.route_short_name
FROM
    stops s
JOIN
    stop_times st ON s.stop_id = st.stop_id
JOIN
    trips t ON st.trip_id = t.trip_id
JOIN
    routes r ON t.route_id = r.route_id
ORDER BY
    s.stop_id, t.route_id;
.output stdout

.output result9.txt
SELECT DISTINCT
    tr.from_stop_id AS transfer_location,
    tr.min_transfer_time AS transfer_time
FROM
    transfers tr;
.output stdout
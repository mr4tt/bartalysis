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
JOIN stop_times st1 ON t.trip_id = st1.trip_id AND st1.stop_id = 'SHAY'
JOIN stop_times st2 ON t.trip_id = st2.trip_id AND st2.stop_id = 'FRMT'
JOIN routes r ON t.route_id = r.route_id
JOIN calendar c ON t.service_id = c.service_id
WHERE c.thursday = 1
AND st1.departure_time > '08:00:00'
AND st1.stop_sequence < st2.stop_sequence
AND '2024-08-12' BETWEEN c.start_date AND c.end_date
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
        WHERE origin_id = 'SHAY'
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
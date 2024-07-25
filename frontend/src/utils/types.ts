export interface stationType {
    "name": string,
    "abbr": string,
    "lat": string,
    "lng": string,
    "address": string,
    "city": string,
    "county": string,
    "state": string,
    "zipcode": string,
}

export interface stationTypeArr {
    points: stationType[]
}

export interface train {
    "ArrivalTime": string,
    "DepartureTime": string,
    "EndingId": string,
    "StartingID": string,
    "TrainColor": string,
    "TrainDescription": string,
    "TrainName": string,
}

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
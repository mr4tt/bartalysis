import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"
import { stationList, findStation } from "../utils/stations"
import { AdvancedMarker, APIProvider, Map, useMap, useMapsLibrary } from '@vis.gl/react-google-maps';
import { useState, useEffect, useRef } from "react"
import Directions from "../components/Directions";
import { Markers } from "../components/Markers";
import { getNextThreeTrains, countDecimals } from "../utils/utils";
import { train } from "../utils/types";
import StationForm from "../components/StationForm";

export default function RoutePlanner() {
    const [trip, setTrip] = useState({ "origin": "", "destination" : "" })
    const [trains, setTrains] = useState<train[]>([])
    const [fares, setFares] = useState([])
    const [flag, setFlag] = useState(false)
    const firstSubmit = useRef(false)
    const position = { lat: 37.668819, lng: -122.080795}

    const handleClick = (e: React.FormEvent) => {
        if (!(trip["origin"] === "" || trip["origin"] === "Select" 
            || trip.destination === "" || trip.destination === "Select")) {
            setFlag(!flag)
            firstSubmit.current = true
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTrip({...trip, [e.target.id]: e.target.value})
        console.log(e.target.id, e.target.value)
    }

    useEffect(() => {
        const fetchData = async() => {
            const response = await fetch(`https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/route-planner/${trip['origin']}/${trip.destination}/?date=2024-08-13&time=08:00:00`)
            const data = await response.json()
            console.log(data)
            const nextThreeTrains = getNextThreeTrains(data.trains)
            // console.log(nextThreeTrains)
            setFares(data.fares)
            setTrains([...nextThreeTrains])

        }
        if (flag) fetchData()
    }, [flag])
  
    // console.log(trains)
    // console.log(trip)
    return (
        <div className="row-span-7 grid grid-cols-5 mt-2">
            <div className="bg-slate-400 grid grid-rows-6 gap-4 col-span-2 border-r-2 border-black py-2 px-6">
                <div className="flex justify-evenly row-span-1">
                    <StationForm location="Origin" handleChange={handleChange}/>
                    <StationForm location="Destination" handleChange={handleChange}/>
                    <button className="border-black border-2 bg-white self-end px-4 py-2 rounded-md 
                    hover:bg-slate-300" onClick={handleClick}>
                        Submit
                    </button>
                </div>

                <div className="bg-slate-400 row-span-5 grid grid-cols-5 gap-2">
                    <div className="grid grid-row-3 gap-2 col-span-3">
                        { trains.map((train: train, i) => <IncomingTrainsContainer train={train} key={i} />)}
                        {/* <div className="border-black border-2 flex flex-col ">
                            <p className=" font-bold text-md">Fares</p>
                            <div className="flex flex-col ">
                               
                            </div>
                        </div> */}
                    </div>
                    <div className="col-span-2 grid gap-2 bg-slate-500 h-min px-4 py-2">
                        <div className="font-bold text-lg">Price</div>
                        { fares.map((fare: any, i) => {
                            return (
                                <div key={i}>
                                    <p className="">{ fare.Description }</p>
                                    <p className="text-sm">${ fare.Price }{ countDecimals(fare.Price) === 1 ? "0" : "" }</p>
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
            
            <div className="col-span-3 h-screen w-full">
                <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
                    <Map
                        center={position}
                        zoom={10}
                        mapId={import.meta.env.VITE_MAP_ID}
                        streetViewControl={false}
                        mapTypeControl={false}
                    >
                        <Markers points={stationList}/>
                        { trip["origin"] && trip.destination && 
                        <Directions flag={flag} firstSubmit={firstSubmit.current} origin={findStation(trip["origin"])} destination={findStation(trip["destination"]) }/> 
                        }
                    </Map>
                </APIProvider>
            </div>
        </div>
    )
}
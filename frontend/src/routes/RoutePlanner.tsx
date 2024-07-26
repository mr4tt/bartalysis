import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"
import { stationList, findStation } from "../utils/stations"
import { AdvancedMarker, APIProvider, Map } from '@vis.gl/react-google-maps';
import { useState, useRef } from "react"
import { AdvancedMarker, APIProvider, Map } from '@vis.gl/react-google-maps';
import { useState, useRef } from "react"
import Directions from "../components/Directions";
import { Markers } from "../components/Markers";
import { getNextThreeTrains, countDecimals, sortFares } from "../utils/utils";
import { train, fare } from "../utils/types";
import StationForm from "../components/StationForm";

export default function RoutePlanner() {
    const [trip, setTrip] = useState({ "origin": "", "destination" : "" })
    const [trains, setTrains] = useState<train[]>([])
    const [fares, setFares] = useState<fare[]>([])
    const [flag, setFlag] = useState(false)
    const firstSubmit = useRef(false)
    const position = { lat: 37.668819, lng: -122.080795 }

    const handleClick = async(e: React.FormEvent) => {
        if (!(trip.origin === "" || trip.origin === "Select" || trip.destination === "" || trip.destination === "Select")) {
    const handleClick = async(e: React.FormEvent) => {
        if (!(trip.origin === "" || trip.origin === "Select" || trip.destination === "" || trip.destination === "Select")) {
            setFlag(!flag)
            firstSubmit.current = true
            const response = await fetch(`https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/route-planner/${trip.origin}/${trip.destination}/?date=2024-08-13&time=08:00:00`)
            const data = await response.json()
            console.log(data)
            const nextThreeTrains = getNextThreeTrains(data.trains)
            // console.log(nextThreeTrains)
            setFares(data.fares)
            setTrains([...nextThreeTrains])
        }
    }

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTrip({...trip, [e.target.id]: e.target.value})
        console.log(e.target.id, e.target.value)
    }
  
    // console.log(trains)
    // console.log(trip)
    return (
        <div className="row-span-7 grid grid-cols-5 mt-2">
            <div className="bg-slate-200 grid grid-rows-6 gap-4 col-span-2 border-r-2 border-black py-2 px-6">
                <div className="flex justify-evenly row-span-1">
                    <StationForm location="Origin" handleChange={handleChange}/>
                    <StationForm location="Destination" handleChange={handleChange}/>
                    <div className="grid items-center">
                        <div></div>
                        <button className="hover:bg-blue-300 border-slate-400 border-2 bg-slate-300 self-center px-3 py-2 rounded-md 
                        " onClick={handleClick}>
                            Submit
                        </button>
                    </div>
                </div>

                <div className="bg-slate-200 row-span-5 grid grid-cols-5 gap-2">
                    <div className="col-span-3 grid grid-rows-10 gap-2">
                        <div className="font-bold row-span-1 bg-slate-300 p-2 flex items-center justify-center">Trains</div>
                        <div className="grid grid-row-3 gap-2 row-span-9">
                        { trains.length !== 0
                            ? trains.map((train: train, i) => <IncomingTrainsContainer train={train} key={i} />)
                            : <div className="bg-slate-300 h-full"></div>
                        }
                        </div>
                    </div>
                    
                    <div className="col-span-2 grid gap-2 grid-rows-10">
                        <p className="bg-slate-300 font-bold grid justify-items-center items-center p-2 row-span-1">Price</p>
                        <div className="bg-slate-300 self-start row-span-9 grid gap-2">
                            { fares.length !== 0 
                                ? fares.map((fare: fare, i) => {
                                    return (
                                        <div className="px-4 py-2" key={i}>
                                            <p className="">{ fare.Description }</p>
                                            <p className="text-sm">${ fare.Price }{ countDecimals(fare.Price) === 1 ? "0" : "" }</p>
                                        </div>
                                    )
                                })
                                : <div className="bg-slate-300 h-full"></div>
                            }
                        </div>
                    </div>
                </div>  
            </div>
            
            <div className="col-span-3 h-screen w-full">
                <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
                    <Map
                        defaultCenter={position}
                        defaultZoom={10}
                        mapId={import.meta.env.VITE_MAP_ID}
                        gestureHandling={'greedy'}
                        disableDefaultUI={true}
                    >
                        <Markers points={stationList}/>
                        { trip.origin && trip.destination && 
                        <Directions flag={flag} firstSubmit={firstSubmit.current} origin={findStation(trip.origin)} destination={findStation(trip["destination"]) }/> 
                        }
                    </Map>
                </APIProvider>
            </div>
        </div>
    )
}
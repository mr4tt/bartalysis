import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"
import { stationList, findStation } from "../utils/stations"
import { AdvancedMarker, APIProvider, Map, useMap, useMapsLibrary } from '@vis.gl/react-google-maps';
import { useState, useEffect, useRef } from "react"
import Directions from "../components/Directions";
import { Markers } from "../components/Markers";
import { getNextThreeTrains } from "../utils/utils";
import { train } from "../utils/types";

export default function RoutePlanner() {
    const [trip, setTrip] = useState({ "starting-point": "", "destination" : "" })
    const [trains, setTrains] = useState<train[]>([])
    const [flag, setFlag] = useState(false)
    const firstSubmit = useRef(false)
    const position = { lat: 37.668819, lng: -122.080795}

    const handleClick = (e: React.FormEvent) => {
        if (!(trip["starting-point"] === "" || trip["starting-point"] === "Select" 
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
            const response = await fetch(`https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/route-planner/${trip['starting-point']}/${trip.destination}/?date=2024-08-13&time=08:00:00`)
            const data = await response.json()
            const nextThreeTrains = getNextThreeTrains(data.trains)
            // console.log(nextThreeTrains)
            setTrains([...nextThreeTrains])
        }
        fetchData()
    }, [flag])

    // console.log(trains)
    // console.log(trip)
    return (
        <div className="row-span-7 grid grid-cols-5 mt-2">
            <div className="bg-slate-400 grid grid-rows-6 gap-4 col-span-2 border-r-2 border-black py-2 px-6">
                <div className="flex justify-evenly row-span-1">
                    {/* make this a component; i need a parameter that changes origin/destination and starting-point??? 
                    maybe I should change starting-point to origin */}
                    <div className="rounded-sm flex justify-center flex-col gap-2">
                        <label htmlFor="starting-point" className="text-lg">Origin</label>
                        <form action="">
                            <select name="starting-point" id="starting-point" onChange={handleChange} className="w-1/2">
                                <option defaultValue={"initial"}>Select</option>
                                { stationList.map((obj, i) => {
                                    return <option value={obj.abbr} key={i}>{obj.name}</option>
                                })}
                            </select>
                        </form>
                    </div>

                    <div className="rounded-sm flex justify-center flex-col gap-2">
                        <label htmlFor="destination" className="text-lg">Destination</label>
                        <form action="">
                            <select name="destination" id="destination" onChange={handleChange} className="w-1/2">
                                <option defaultValue={"initial"}>Select</option>
                                { stationList.map((obj, i) => {
                                    return <option value={obj.abbr} key={i}>{obj.name}</option>
                                })}
                            </select>
                        </form>
                    </div>

                    <button className="border-black border-2 bg-white self-end px-4 py-2 rounded-md 
                    hover:bg-slate-300" onClick={handleClick}
                    >
                        Submit
                    </button>
                </div>

                <div className="bg-slate-400 row-span-5 grid gap-2">
                    <div className="grid grid-row-3 gap-2">
                        { trains.map((train: train, i) => <IncomingTrainsContainer train={train} key={i} />)}
                        {/* <div className="border-black border-2 flex flex-col ">
                            <p className=" font-bold text-md">Fares</p>
                            <div className="flex flex-col ">
                               
                            </div>
                        </div> */}
                    </div>
                </div>
            </div>
            
            <div className="col-span-3 h-screen w-full">
                <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
                    <Map
                        center={position}
                        zoom={10}
                        mapId={import.meta.env.VITE_MAP_ID}
                    >
                        <Markers points={stationList}/>
                        { trip["starting-point"] && trip.destination && 
                        <Directions flag={flag} firstSubmit={firstSubmit.current} origin={findStation(trip["starting-point"])} destination={findStation(trip["destination"]) }/> 
                        }
                    </Map>
                </APIProvider>
            </div>
        </div>
    )
}
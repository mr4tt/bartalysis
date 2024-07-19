import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"
import { stationList, findStation } from "../utils/stations"
import { AdvancedMarker, APIProvider, Map, useMap, useMapsLibrary } from '@vis.gl/react-google-maps';
import { useState, useEffect } from "react"
import Directions from "../components/Directions";
import { Markers } from "../components/Markers";

export default function RoutePlanner() {
    const [trip, setTrip] = useState({ "starting-point": "", "destination" : "" })

    const handleClick = (e: React.FormEvent) => {
        console.log('handle click')
        // when this is triggered, maybe change a state which is a dependency in a useEffect
        // where that useEffect fetches the data from our api
    }

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTrip({...trip, [e.target.id]: e.target.value})
        console.log(e.target.id, e.target.value)
    }

    // useEffect(() => {
    //     const fetchData = async() => {
    //         const response = await fetch('https://bug-free-space-meme-956jrx6xpjx29xr4-8000.app.github.dev/api/departures/')
    //         const data = await response.json()
    //         console.log(data)
    //     }
    //     fetchData()
    // }, [])

    return (
        <div className="row-span-7 grid grid-cols-5">
            <div className="bg-slate-400 grid grid-rows-6 gap-4 mt-2 col-span-2 border-r-2 border-black py-2 px-6">
                <div className="flex justify-evenly row-span-1">
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

                <div className="bg-slate-400 row-span-5 grid grid-cols-5 gap-2">
                    <div className="col-span-1 grid grid-rows-5 ">
                        <p className="row-span-1 font-bold border-b-2 border-black">Trains</p>
                        <p className="row-span-4 font-bold border-b-2 border-black">Departing</p>
                    </div>
                    <div className="flex justify-evenly col-span-4 gap-2">
                        <IncomingTrainsContainer />
                        <IncomingTrainsContainer />
                        <IncomingTrainsContainer />
                        {/* <div className="border-black border-2 flex flex-col ">
                            <p className=" font-bold text-md">Fares</p>
                            <div className="flex flex-col ">
                               
                            </div>
                        </div> */}
                    </div>
                </div>
            </div>
            
            <div className="col-span-3">

            </div>
        </div>
    )
}
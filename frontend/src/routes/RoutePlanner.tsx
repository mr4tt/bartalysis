import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"
import { stationList } from "../utils/stations"
import { useState } from "react"

export default function RoutePlanner() {
    const [trip, setTrip] = useState({ "starting-point": "", "destination" : "" })

    const handleClick = (e: React.FormEvent) => {
        console.log('handle click')
        // when this is triggered, maybe change a state which is a dependency in a useEffect
        // where that useEffect fetches the data from our api
    }

    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        setTrip({...trip, [e.target.id]: e.target.value})
    }

    return (
        <div className="  row-span-7 grid grid-rows-6 gap-12">
            <div className="flex justify-around row-span-2">
                <div className=" bg-slate-400 w-2/5 px-12 py-6 rounded-sm">
                    <label htmlFor="starting-point">Choose your starting point</label>
                    <form action="">
                        <select name="starting-point" id="starting-point" onChange={handleChange}>
                            <option defaultValue={"initial"}>Select</option>
                            { stationList.map((obj, i) => {
                                return <option value={obj.abbreviation} key={i}>{obj.station}</option>
                            })}
                        </select>
                    </form>
                </div>

                <div className=" bg-slate-400 w-2/5 px-12 py-6 rounded-sm">
                    <label htmlFor="destination">Choose your destination</label>
                    <form action="">
                        <select name="destination" id="destination" onChange={handleChange}>
                            <option defaultValue={"initial"}>Select</option>
                            { stationList.map((obj, i) => {
                                return <option value={obj.abbreviation} key={i}>{obj.station}</option>
                            })}
                        </select>
                    </form>
                </div>

                <button className="border-black border-2 self-center px-4 py-2 rounded-md 
                hover:bg-slate-300" onClick={handleClick}
                >
                    Submit
                </button>
            </div>

            <div className="bg-slate-400 row-span-4 grid grid-cols-5 p-4">
                <div className="col-span-1 grid grid-rows-5 ">
                    <p className="row-span-1">Trains</p>
                    <p className="row-span-4">Departing</p>
                </div>
                <div className="flex justify-evenly col-span-4">
                    <IncomingTrainsContainer />
                    <IncomingTrainsContainer />
                    <IncomingTrainsContainer />
                    <div className="border-black border-2 p-8 flex flex-col gap-4">
                        <p className=" font-bold text-lg">Fares</p>
                        <div className="flex flex-col gap-4">
                            <div>4.40</div>
                            <div>2.20</div>
                            <div>1.90</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
import React from "react"
import IncomingTrainsContainer from "../components/IncomingTrainsContainer"

export default function RoutePlanner() {

    return (
        <div className="  row-span-7 grid grid-rows-6 gap-12">
            <div className="flex justify-around row-span-2">
                <div className=" bg-slate-400 w-2/5 px-12 py-6 rounded-sm">
                    <label htmlFor="starting-point">Choose your starting point</label>
                    <form action="">
                        <select name="starting-point" id="starting-point">
                            <option value="initial" selected>Select</option>
                            <option value="bay-fair">Bay Fair</option>
                            <option value="san-leandro">San Leandro</option>
                            <option value="hayward">Hayward</option>
                            <option value="union-city">union-city</option>
                            <option value="south-hayward">South Hayward</option>
                            <option value="fremont">Fremont</option>
                        </select>
                    </form>
                </div>

                <div className=" bg-slate-400 w-2/5 px-12 py-6 rounded-sm">
                    <label htmlFor="destination">Choose your destination</label>
                    <form action="">
                        <select name="destination" id="destination">
                            <option value="initial" selected>Select</option>
                            <option value="bay-fair">Bay Fair</option>
                            <option value="san-leandro">San Leandro</option>
                            <option value="hayward">Hayward</option>
                            <option value="union-city">union-city</option>
                            <option value="south-hayward">South Hayward</option>
                            <option value="fremont">Fremont</option>
                        </select>
                    </form>
                </div>
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
                </div>
            </div>
        </div>
    )
}
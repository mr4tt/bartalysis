import React from "react";
import { stationList } from "../utils/stations";

export default function StationForm({ handleChange, location }: { handleChange: React.ChangeEventHandler<HTMLSelectElement>, location: string }) {

    return (
        <div className="rounded-sm flex justify-center flex-col gap-2">
            <label htmlFor={`${location.toLowerCase()}`} className="text-lg">{ location }</label>
            <form action="">
                <select name={`${location.toLowerCase()}`} id={`${location.toLowerCase()}`} onChange={ handleChange } className="w-1/2 rounded-sm px-2 py-1">
                    <option defaultValue={"initial"}>Select</option>
                    { stationList.map((obj, i) => {
                        return <option value={obj.abbr} key={i}>{obj.name}</option>
                    })}
                </select>
            </form>
        </div>
    )
}
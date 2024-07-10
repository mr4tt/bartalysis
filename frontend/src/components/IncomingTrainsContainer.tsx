import React from "react";

// probably need a counter for the incoming train and the minutes, 
// i'll just use .map later when we have the actual data
// parameters: destination (string), trains (array of objects)
export default function IncomingTrainsContainer() {
    return (
        <div className="grid grid-rows-5 bg-slate-600 px-8 py-6 rounded-sm">
            <div className="row-span-1">Destination</div>
            <div className="row-span-4 grid gap-2 justify-items-center">
                <div className="">
                    <p>Incoming train #1:</p>
                    <p>X mins</p>
                </div>
                <div className="">
                    <p>Incoming train #2:</p>
                    <p>X mins</p>
                </div>
                <div className="">
                    <p>Incoming train #3:</p>
                    <p>X mins</p>
                </div>
            </div>
        </div>
    )
}
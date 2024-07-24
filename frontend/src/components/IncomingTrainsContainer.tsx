import React from "react";

export default function IncomingTrainsContainer({ train }: any) {
    return (
        <div className="bg-slate-500 px-4 py-2 grid gap-2">
            <p>Train color: {train.TrainName.slice(0, train.TrainName.length - 2)}</p>
            <div className="flex justify-between">
                <p>Incoming at: <span className="font-bold">{train.DepartureTime}</span></p>
                <p>ETA: <span className="font-bold">{train.ArrivalTime}</span></p>
            </div>
            <p>{train.TrainDescription}</p>
        </div>
    )
}
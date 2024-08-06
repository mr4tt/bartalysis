import React from "react";
import { train } from "../utils/types";
import { updateTime } from "../utils/utils";

export default function IncomingTrainsContainer({ train }: { train: train }) {
    return (
        <div className="bg-slate-300 px-4 py-2 grid gap-2 items-center">
            <p>{train.TrainDescription}</p>
            <p>Train color: {train.TrainName.slice(0, train.TrainName.length - 2)}</p>
            <div className="flex justify-between items-center">
                <p>Incoming at: <span className="font-bold">{updateTime(train.DepartureTime)}</span></p>
                <p>ETA: <span className="font-bold">{updateTime(train.ArrivalTime)}</span></p>
            </div>
        </div>
    )
}
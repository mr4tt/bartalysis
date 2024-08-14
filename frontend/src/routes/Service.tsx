import React from "react";

export default function Service() {
    const lines = ["red", "orange", "yellow","green", "blue"]

    return (
        <div className="row-span-7 p-8">
            <div className="border-black border-2 ">
                    <div className="border-black border-2 grid grid-cols-5">
                        <div className=" font-bold">Train</div>
                        <div className=" font-bold">Active</div>
                        <div className=" font-bold">Avg. wait</div>
                        <div className=" font-bold">Tardy (%)</div>
                        <div className=" font-bold">Avg. wait</div>
                    </div>
                    {lines.map((line, i) => {
                        return (
                            <div key={i} className={`border-black border-2 bg-${line}-400 grid grid-cols-5`}>
                                <div className="">{line}</div>
                                <div className="">hi1</div>
                                <div className="">hi2</div>
                                <div className="">hi3</div>
                                <div className="">hi4</div>
                            </div>
                        )
                    })}
            </div>
        </div>
    )
}
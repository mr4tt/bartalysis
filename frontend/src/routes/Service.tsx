import React from "react";


// parameters will be the data
// probably need to have a trains object corresponds to each object in the data
export default function Service() {
    const lines = ["red", "orange", "yellow","green", "blue"]

    return (
        <div className="row-span-7 p-8">
            <table className="border-black border-2">
                <tbody>
                    <tr className="border-black border-2">
                        <th className="border-black border-2">Train</th>
                        <th className="border-black border-2">Active</th>
                        <th className="border-black border-2">Avg. wait</th>
                        <th className="border-black border-2">Tardy (%)</th>
                        <th className="border-black border-2">Avg. wait</th>
                    </tr>
                    {lines.map((line, i) => {
                        return (
                            <tr key={i} className={`border-black border-2 bg-${line}-400`}>
                                <td className="border-black border-2">{line}</td>
                                <td className="border-black border-2">hi1</td>
                                <td className="border-black border-2">hi2</td>
                                <td className="border-black border-2">hi3</td>
                                <td className="border-black border-2">hi4</td>
                            </tr>
                        )
                    })}
                </tbody>
            </table>
        </div>
    )
}
import React from "react"
import PinMarker from "./PinMarker"
import { stationTypeArr, stationType } from "../utils/types"

export function Markers({ points }: stationTypeArr){
  return (
    <>
      { points.map((point: stationType, i: number) => {
        return (
        <div key={i} >
         <PinMarker point={point}/>
        </div>
        )
      })}
    </>
  )
}
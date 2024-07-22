import React from "react"
import PinMarker from "./PinMarker"

export function Markers({ points }: any){
  return (
    <>
      { points.map((point: any, i: number) => {
        return (
        <div key={i} >
         <PinMarker point={point}/>
        </div>
        )
      })}
    </>
  )
}
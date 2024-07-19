import React from "react"
import { AdvancedMarker } from "@vis.gl/react-google-maps"

export function Markers({ points }: any){
    return (
      <>
        { points.map((point: any, i: number) => {
          return (
            <AdvancedMarker position={{ lat: parseFloat(point.lat), lng: parseFloat(point.lng)}} key={i}>
            
              <span>🚂</span>
            </AdvancedMarker>
          )
        })}
      </>
    )
  }
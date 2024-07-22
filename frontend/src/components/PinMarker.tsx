import React from "react"
import { AdvancedMarker, InfoWindow } from "@vis.gl/react-google-maps"
import bartLogo from "../assets/img/bart-logo.png"
import { useState } from "react"

export default function PinMarker({ point }: { point: any}) {
    const [open, setOpen] = useState(false)

    return (
        <div>
            <AdvancedMarker position={{ lat: parseFloat(point.lat), lng: parseFloat(point.lng) }} onClick={() => setOpen(true)}>
                <img src={bartLogo} alt="Bart logo" className=" w-5"/>
            </AdvancedMarker>

            { open && 
            <InfoWindow position={{ lat: parseFloat(point.lat), lng: parseFloat(point.lng) }} 
                onCloseClick={() => setOpen(false)} className="h-min">
                {point.name} Bart station
            </InfoWindow>}
        </div>
    )
}
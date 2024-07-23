
import { useMap, useMapsLibrary } from "@vis.gl/react-google-maps"
import { useState, useEffect } from "react"
import { stationType } from "../utils/types"

export default function Directions({ origin, destination, flag } : { origin: stationType | undefined, destination: stationType | undefined, flag: boolean}) {
    const map = useMap()
    const routesLibrary = useMapsLibrary("routes")
    const [directionsService, setDirectionsService] = useState<google.maps.DirectionsService>()
    const [directionsRenderer, setDirectionsRenderer] = useState<google.maps.DirectionsRenderer>()
    const [routes, setRoutes] = useState<google.maps.DirectionsRoute[]>([])
  
    useEffect(() => {
      if (!routesLibrary || !map) return
      setDirectionsService(new routesLibrary.DirectionsService())
      setDirectionsRenderer(new routesLibrary.DirectionsRenderer({ map }))
    }, [routesLibrary, map])
  
    useEffect(() => {
      if (!directionsService || !directionsRenderer) return
  
      directionsService.route({
        origin: { lat: parseFloat(origin?.lat ?? '0'), lng: parseFloat(origin?.lng ?? '0') },
        destination: { lat: parseFloat(destination?.lat ?? '0'), lng: parseFloat(destination?.lng ?? '0') },
        travelMode: google.maps.TravelMode.DRIVING,
        provideRouteAlternatives: true,
      }).then((response) => {
        directionsRenderer.setDirections(response)
        setRoutes(response.routes)
      })
    }, [directionsService, directionsRenderer, flag])
  
    // console.log(routes)
    return (null)
  }
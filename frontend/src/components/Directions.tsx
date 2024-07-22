
import { useMap, useMapsLibrary } from "@vis.gl/react-google-maps"
import { useState, useEffect } from "react"

export default function Directions({ origin, destination } : any) {
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
        origin: { lat: parseFloat(origin.lat), lng: parseFloat(origin.lng) },
        destination: { lat: parseFloat(destination.lat), lng: parseFloat(destination.lng) },
        travelMode: google.maps.TravelMode.DRIVING,
        provideRouteAlternatives: true,
      }).then((response) => {
        directionsRenderer.setDirections(response)
        setRoutes(response.routes)
      })
    }, [directionsService, directionsRenderer, origin, destination])
  
    // console.log(routes)
    return (null)
  }
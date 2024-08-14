
import { useMap, useMapsLibrary } from "@vis.gl/react-google-maps"
import { useState, useEffect } from "react"
import { stationType } from "../utils/types"

export default function Directions({ origin, destination, flag, firstSubmit, trainColor } : 
  { origin: stationType | undefined, destination: stationType | undefined, flag: boolean, firstSubmit: boolean, trainColor: string }) {
    const map = useMap()
    const routesLibrary = useMapsLibrary("routes")
    const [directionsService, setDirectionsService] = useState<google.maps.DirectionsService>()
    const [directionsRenderer, setDirectionsRenderer] = useState<google.maps.DirectionsRenderer>()
    const [routes, setRoutes] = useState<google.maps.DirectionsRoute[]>([])
  
    useEffect(() => {
      if (!routesLibrary || !map) return
      const service = new routesLibrary.DirectionsService()
      const renderer = new routesLibrary.DirectionsRenderer({
        map,
        polylineOptions: {
          strokeColor: `#${trainColor}`, 
          strokeOpacity: 1.0,
          strokeWeight: 8,
        }
      })
      setDirectionsService(service)
      setDirectionsRenderer(renderer)
      
      return () => {
        renderer.setMap(null)
      }
    }, [routesLibrary, map, trainColor])
  
    useEffect(() => {
      if (!directionsService || !directionsRenderer || !firstSubmit) return

      const emptyDirectionsResult: google.maps.DirectionsResult = {
        routes: [],
        request: {origin: "", destination: "", travelMode: google.maps.TravelMode.TRANSIT},
        geocoded_waypoints: []
      }
      directionsRenderer.setDirections(emptyDirectionsResult)
  
      directionsService.route({
        origin: { lat: parseFloat(origin?.lat ?? '0'), lng: parseFloat(origin?.lng ?? '0') },
        destination: { lat: parseFloat(destination?.lat ?? '0'), lng: parseFloat(destination?.lng ?? '0') },
        travelMode: google.maps.TravelMode.TRANSIT,
        provideRouteAlternatives: true
      }).then((response) => {
        directionsRenderer.setDirections(response)
        setRoutes(response.routes)
      })
    }, [directionsService, directionsRenderer, flag, trainColor])
  
    return (null)
}
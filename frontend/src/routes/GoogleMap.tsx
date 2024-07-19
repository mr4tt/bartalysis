import React from 'react';
import { createRoot } from 'react-dom/client';
import { AdvancedMarker, APIProvider, Map, useMap, useMapsLibrary } from '@vis.gl/react-google-maps';
import { useEffect, useState } from 'react';
import { stationList } from '../utils/stations';

export default function GoogleMap() {
  const position = { lat: 37.668819, lng: -122.080795}

  // watch the first vid in the google maps playlist to learn how to create the information bubble on each marker
  return (
    <div className="h-screen w-full">
      <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
      <Map
        center={position}
        zoom={10}
        mapId={import.meta.env.VITE_MAP_ID}
      >
        {/* <Markers points={stationList}/> */}
        <Directions />
      </Map>
    </APIProvider>
    </div>

    
  )
}

const Markers = ({ points }: any) => {

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

const Directions = () => {
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
      origin: "1620 Berryessa Road",
      destination: "500 John Daly Blvd.",
      travelMode: google.maps.TravelMode.DRIVING,
      provideRouteAlternatives: true,
    }).then((response) => {
      directionsRenderer.setDirections(response)
      setRoutes(response.routes)
    })
  }, [directionsService, directionsRenderer])

  console.log(routes)
  return (null)
}
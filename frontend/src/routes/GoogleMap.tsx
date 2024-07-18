import React from 'react';
import { createRoot } from 'react-dom/client';
import { AdvancedMarker, APIProvider, Map } from '@vis.gl/react-google-maps';
import { useEffect } from 'react';
import { stationList } from '../utils/stations';

export default function GoogleMap() {
  const position = { lat: 37.668819, lng: -122.080795}

  return (
    <div className="h-screen w-full">
      <APIProvider apiKey={import.meta.env.VITE_GOOGLE_MAPS_API_KEY}>
      <Map
        center={position}
        zoom={10}
        mapId={import.meta.env.VITE_MAP_ID}
      >
        <Markers points={stationList}/>
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
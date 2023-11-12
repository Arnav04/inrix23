import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Map = () => {
  const position = [37.773972, 	-122.431297]; // Centered on SF

    // // Define a filter function to exclude certain POIs
    // const poiFilter = function (feature, layer) {
    //     return feature.properties.amenity !== 'restaurant' || !feature.properties.natural;
    // };

  return (
    <MapContainer
      center={position}
      zoom={13}
      style={{ position:'absolute', height: '100vh', width: '100%' }}
    >
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        // filter={poiFilter}
      />

      <Marker position={position}>
        <Popup>
          A pretty CSS3 popup. <br /> Easily customizable.
        </Popup>
      </Marker>
      
    </MapContainer>
  );
};

export default Map;

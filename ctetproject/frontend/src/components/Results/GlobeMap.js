// GlobeMap.js
import React, { useRef, useEffect } from "react";
import mapboxgl from "mapbox-gl";
import "./Results.css";

//import and setup mapbox access key
import config from "../../config.js";
mapboxgl.accessToken = config.MAPBOX_SECRET_KEY;

const GlobeMap = ({ cities, colors }) => {
  const mapContainer = useRef(null);

  //create globe 3d map, using person style studio globe
  useEffect(() => {

    //adjust zoom level of the globe based on screen width
    const getZoomLevel = () => {
      const screenWidth = window.innerWidth;
      if (screenWidth < 600) {
        return 1;
      } else if (screenWidth < 1000) {
        return 1.5;
      } else {
        return 2;
      }
    };
    const initialZoom = getZoomLevel();

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: "mapbox://styles/samman-pali/cluuou662005b01om13hvc4q4",
      center: [0, 0],
      zoom: initialZoom,
      pitch: 0,
      bearing: 0,
      // remove reference marker
      attributionControl: false,
      projection: { name: "globe" },
    });

    

    //adding markers for cities array
    cities.forEach((city, index) => {
      // create a DOM element for each marker
      const marker_element = document.createElement("div");
      marker_element.className = "map-marker";

      // cnclude an SVG pin marker icon as opposed to default
      marker_element.innerHTML = `<svg viewBox="0 0 24 24" width="38" height="38" stroke="black" stroke-width="2" fill="${
        colors[index % colors.length]
      }" stroke-linecap="round" stroke-linejoin="round" class="css-i6dzq1"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
        <span class="marker-label">${city.name}</span>`;

      if (index === 0) {
        map.setCenter(city.coordinates)
      }
      // add the marker to the map
      new mapboxgl.Marker(marker_element)
        .setLngLat(city.coordinates)
        .addTo(map);
      });

    // remove navigation controls from the map
    map.removeControl(new mapboxgl.NavigationControl());

    return () => map.remove();
  }, [cities, colors]);

  return <div ref={mapContainer} id="map-container" />;
};

export default GlobeMap;

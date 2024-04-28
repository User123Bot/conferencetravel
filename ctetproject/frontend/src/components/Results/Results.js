import React from "react";
import GlobeMap from "./GlobeMap";
import "./Results.css";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEmissions } from '../../EmissionsContext';

// PLACEHOLDER ONLY FOR TESTING UNTIL ALGORITHM IS INTEGRATED:
// const cities = [
//   { name: "New York", coordinates: [-74.006, 40.7128], emissions: 1234 },
//   { name: "London", coordinates: [-0.1276, 51.5072], emissions: 2345 },
//   { name: "Paris", coordinates: [2.352222, 48.856613], emissions: 3456 },
//   { name: "Sydney", coordinates: [151.209295, -33.86882], emissions: 4567 },
//   { name: "Cairo", coordinates: [31.235712, 30.04442], emissions: 5678 },
// ];

const colors = ["#F7DD72", "#FD9689", "#90E89F", "#BEA0E5", "#C9DDFF"];

function Results() {
  const {emissionsData } = useEmissions();

  const transformedData = emissionsData.map((destination) => ({
    name: destination.Destination,
    coordinates: [destination.Lng, destination.Lat],
    emissions: destination.Total_Emissions_kg_CO2e,
  }))
  
  return (
    <section id="results" className="results-section">
      <div className="results-content">
        <div className="results-title">
          <h1>Calculated Emissions Results</h1>
        </div>
        <div className="results-body">
          <p>
            Here's how we've ranked conference locations based on increasing
            carbon emissions:
          </p>
        </div>
        {/* Display cities as tiles */}
        <div className="city-tiles">
          {emissionsData.map((destination, index) => (
            <div
              key={index}
              className="city-tile"
            >
              <span className="city-tile-index">
                {index + 1}
              </span>
              <span className="city-tile-name" style={{ backgroundColor: colors[index % colors.length] }}>
                {destination.Destination}
              </span>
              <span className="city-tile-emissions" >
                CO<sub>2</sub> Emissions: {destination.Total_Emissions_kg_CO2e} kg
              </span>
            </div>
          ))}
        </div>
      </div>
      {/* Pass cities and colors as props to GlobeMap */}
      <GlobeMap cities={transformedData} colors={colors} />
    </section>
  );
}

export default Results;

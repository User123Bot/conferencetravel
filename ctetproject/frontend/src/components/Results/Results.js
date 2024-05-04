import React from "react";
import GlobeMap from "./GlobeMap";
import "./Results.css";
import "mapbox-gl/dist/mapbox-gl.css";
import { useEmissions } from '../../EmissionsContext';

const colors = ["#F7DD72", "#FD9689", "#90E89F", "#BEA0E5", "#C9DDFF"];

function Results() {
  const {emissionsData } = useEmissions();

  // helper function to format data between kilograms and tonnes
  const formatEmissions = (emissions) => {
    if (emissions >= 10000) {
      // tonnes conversion, 2dp
      return `${(emissions / 1000).toFixed(2)} Tonnes`;
    } else {
      return `${emissions} Kilograms`;
    }
  }

  const transformedData = emissionsData.map((destination) => ({
    name: destination.Destination,
    coordinates: [destination.Lng, destination.Lat],
    emissions: formatEmissions(destination.Total_Emissions_kg_CO2e),
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
                CO<sub>2</sub> Emissions: {formatEmissions(destination.Total_Emissions_kg_CO2e)}
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

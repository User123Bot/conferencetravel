// Calculator.js
import React, { useState, useEffect } from "react";
import { useTransition, animated } from "@react-spring/web";
import { useEmissions } from '../../EmissionsContext';
import "./Calculator.css";


const ManualCarousel = ({ children }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [direction, setDirection] = useState('right');
  const [isAnimating, setIsAnimating] = useState(false);

  const goToPrevious = () => {
    if (!isAnimating) {
      setDirection('left');
      setCurrentIndex((prevIndex) => (prevIndex - 1 + children.length) % children.length);
    }
  };

  const goToNext = () => {
    if (!isAnimating) {
      setDirection('right');
      setCurrentIndex((prevIndex) => (prevIndex + 1) % children.length);
    }
  };

  const goToIndex = (index) => {
    if (!isAnimating && index !== currentIndex) {
      setDirection(index > currentIndex ? 'right' : 'left');
      setCurrentIndex(index);
    }
  };

  const transitions = useTransition(currentIndex, {
    from: { opacity: 0, transform: direction === 'right' ? 'translate3d(100%,0,0)' : 'translate3d(-100%,0,0)' },
    enter: { opacity: 1, transform: 'translate3d(0%,0,0)' },
    leave: { opacity: 0, transform: direction === 'right' ? 'translate3d(-100%,0,0)' : 'translate3d(100%,0,0)' },
    keys: currentIndex,
    onStart: () => setIsAnimating(true),
    onRest: () => setIsAnimating(false)
  });

  const renderNavigationDots = () => {
    return children.map((_, index) => (
      <span
        key={index}
        className={`nav-dot ${currentIndex === index ? 'active' : ''}`}
        onClick={() => goToIndex(index)}
      />
    ));
  };
  
  // Render the carousel with the current slide based on currentIndex
  return (
    <div className="manual-carousel-container">
      <button onClick={goToPrevious} className="arrow left-arrow" disabled={isAnimating}>
        &lt;
      </button>
      {transitions((styles, i) => (
        <animated.div className="slide" style={styles}>
          {children[i]}
        </animated.div>
      ))}
      <button onClick={goToNext} className="arrow right-arrow" disabled={isAnimating}>
        &gt;
      </button>
      <div className="nav-dots">
        {renderNavigationDots()}
      </div>
    </div>
  );
};

const Calculator = () => {
  // gues details
  const [attendees, setAttendees] = useState("");
  const [originCity, setOriginCity] = useState("");
  const [guestInformation, setguestInformation] = useState([]); 

  const { setEmissionsData } = useEmissions();

  const [preferredCities, setPreferredCities] = useState([]);
  const [cityInput, setCityInput] = useState("");
  const [cityPlaceholder, setCityPlaceholder] = useState("Preferred Host City");
  const [fullListNotification, setFullListNotification] = useState("");


  // Ideal conf. location item colours.
  // const colors = ["#3B3E54", "#51546b", "#3B3E54", "#51546b", "#3B3E54"]; //greyscale
  const colors = ["#F7DD72", "#FD9689", "#90E89F", "#BEA0E5", "#C9DDFF"]; //colourful
  const [availableColors, setAvailableColors] = useState([...colors]);

  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadResult, setUploadResult] = useState(null);

  // autocomplete suggestions city data
  const [suggestions, setSuggestions] = useState([]);
  const [cityData, setCityData] = useState([]);
  // keyboard events for suggestion
  const [highlightedIndex, setHighlightedIndex] = useState(-1);

  const [originCitySuggestions, setOriginCitySuggestions] = useState([]);

  // Using React Spring's useTransition to animate the preferred-city-list
  const transitions = useTransition(preferredCities, {
    from: { opacity: 0, transform: 'translate3d(0,-40%,0)' },
  enter: { opacity: 1, transform: 'translate3d(0,0,0)' },
  leave: { opacity: 0, transform: 'translate3d(-100%,0,0)' },
  config: { duration: 500 }, // Duration of 500ms for each transition
  keys: preferredCities.map((city) => city.name),
  });

  const handleKeyDown = (e) => {
    if (e.keyCode === 40 && highlightedIndex < suggestions.length - 1) {
      // down arrow
      setHighlightedIndex(highlightedIndex + 1);
    } else if (e.keyCode === 38 && highlightedIndex > 0) {
      // up arrow
      setHighlightedIndex(highlightedIndex - 1);
    } else if (e.keyCode === 13 && highlightedIndex >= 0) {
      // enter key
      selectSuggestion(suggestions[highlightedIndex]);
    }
  };

  //load cities from JSON file
  useEffect(() => {
    const loadCityData = async () => {
      const response = await fetch("/worldcities.json");
      const cities = await response.json();
      setCityData(cities);
      console.log(cities);
    };

    loadCityData();
  }, []);

  const handleCityInputChange = (e) => {
    const input = e.target.value;
    setCityInput(input);
    setHighlightedIndex(-1);

    if (input.length > 2) {
      // Ensure city names are also converted to uppercase before comparison
      const filteredSuggestions = cityData
        .filter((city) =>
          city.city.toLowerCase().startsWith(input.toLowerCase())
        )
        .slice(0, 5);
      setSuggestions(filteredSuggestions);
      console.log("Filtered suggestions:", filteredSuggestions); // Debug: Logs the suggestions
    } else {
      setSuggestions([]);
    }
  };

  const selectSuggestion = (suggestion) => {
    setCityInput(suggestion.city);
    handleAddCity(suggestion.city);
    setSuggestions([]);
    setHighlightedIndex(-1);
  };

  const isCityValid = (cityName, countryName) => {
    return cityData.some(city => 
      city.city.toLowerCase() === cityName.toLowerCase() &&
      city.country.toLowerCase() === countryName.toLowerCase()
    );
  };
  

  const handleAddGuestInfo = () => {
    const numAttendees = parseInt(attendees);
    if (isNaN(numAttendees) || numAttendees <= 0) {
      alert("Please enter a valid number of attendees greater than zero.");
      return;
    }
    // Check if input fields are not empty
    if (!attendees || !originCity) {
      alert('Please fill in all fields.');
      return;
    }

    if (!uploadResult) {
      setUploadResult({ results: { data: [] } });
    }

    const cityComponents = originCity.split(',');
    if (cityComponents.length < 2) {
      alert('Please make sure to enter both city and country in the format "Country, City".');
      return;
    }
  
    const countryName = cityComponents[0].trim();
    const cityName = cityComponents[1].trim();
  
    if (!isCityValid(countryName, cityName)) {
      alert('The origin city and country combination is not valid. Please select a valid city and country from the suggestions.');
      return;
    }
  
    // Find if the origin city already exists in the results
  const existingCityIndex = uploadResult && uploadResult.results ? uploadResult.results.data.findIndex(row => row.city === originCity.split(',')[0]) : -1;
  
  if (existingCityIndex !== -1) {
    // If the city exists, update the number of attendees
    const updatedData = uploadResult.results.data.map((row, index) => {
      if (index === existingCityIndex) {
        // Update the number of attendees for the existing city
        return {
          ...row,
          number: parseInt(row.number) + parseInt(attendees)
        };
      } else {
        return row;
      }
    });

    setUploadResult((prevUploadResult) => ({
      ...prevUploadResult,
      results: {
        ...prevUploadResult.results,
        data: updatedData
      }
    }));
  } else {
    // If the city doesn't exist, add a new entry
    const newEntry = {
      city: originCity.split(',')[0], 
      country: originCity.split(',')[1] || '', 
      number: attendees
    };

    // Check if uploadResult.results is not null before trying to spread it
    const updatedData = uploadResult && uploadResult.results ? [...uploadResult.results.data, newEntry] : [newEntry];

    setUploadResult((prevUploadResult) => ({
      ...prevUploadResult,
      results: {
        ...prevUploadResult.results,
        data: updatedData
      }
    }));
  }
  
  // Clear the input fields
  setAttendees('');
  setOriginCity('');
  };
  
  const handleRemoveCity = (indexToRemove) => {
    const cityToRemove = preferredCities[indexToRemove];
    // Add the color back to the available colors
    setAvailableColors([...availableColors, cityToRemove.color]);
    setPreferredCities((preferredCities) =>
      preferredCities.filter((_, index) => index !== indexToRemove)
    );
    if (preferredCities.length <= 5) {
      setCityPlaceholder("Preferred Host City");
      setFullListNotification("");
    }
  };

  // Handler for adding a new preferred city
  const handleAddCity = (newCityName) => {
    const cityAlreadyAdded = preferredCities.some(
      (city) => city.name.toUpperCase() === newCityName.toUpperCase()
    );

    if (preferredCities.length >= 5) {
      setFullListNotification("You can only add up to 5 preferred cities.");
      setCityPlaceholder("");
    } else if (newCityName && !cityAlreadyAdded) {
      const newColor = availableColors.shift();
      const newCity = {
        name: newCityName,
        color: newColor,
      };
      setPreferredCities((preferredCities) => [...preferredCities, newCity]);
      setCityInput("");
      setCityPlaceholder("Preferred Host City");
      setFullListNotification("");
    } else {
      setCityInput("");
      setCityPlaceholder(cityAlreadyAdded ? "Try Another" : "Enter City Name");
    }

    setCityInput("");
  };

  // Handler for file upload
  const handleFileUpload = (event) => {
    const file = event.target.files[0];

    if (!file) {
      // TODO: PLEASE CHANGE ALERTS TO BUILT-IN WEBSITE TEXT!
      alert("Please select a file first!");
      return;
    }

    setSelectedFile(file);

    const formData = new FormData();
    formData.append("csv_file", file);

    fetch("http://localhost:8000/api/upload-csv/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        setUploadResult(data);
        updateGuestInformationCSV(data)
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };


  //this is where we will call to backend to get the emissions algo stuff
  const handleCalculateEmissions = async () => {
    // toggling loading cursor to indicate a brief wait period
    document.body.classList.add('loading-cursor')

    console.log("Calculate Button Clicked")
    // these are the preferred cities that'll be passed into backend
    const formattedPreferredCities = preferredCities.map(city => city.name)
    // these are guest details that'll be passed into backend
    const formattedguestInformation = guestInformation.map(city => [city.name, city.attendees])


    const endpoint = 'http://localhost:8000/calculate-emissions/'
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          destinations: formattedPreferredCities,
          origins: formattedguestInformation,
        }),
      });
  
      // error with connection/parsing, http based
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const results = await response.json();
      if (results) {
        console.log("Emissions Calculation Results:", results);
        // on completion of the calculation, scroll into results section
        document.getElementById('results').scrollIntoView({ behavior: 'smooth' })
        setEmissionsData(results.total_emissions);
        // remove loading cursor, indicate completion
        document.body.classList.remove('loading-cursor');
      }

    } catch (error) {
      // reset cursor for error
      document.body.classList.remove('loading-cursor');
      // TODO: make this an built-in website text message
      console.error("Failed to calculate emissions:", error);
    }
  };


  const handleOriginCityChange = (e) => {
    const input = e.target.value;
    setOriginCity(input);
    if (input.length > 2) {
        const filteredSuggestions = cityData.filter(city =>
            city.city.toLowerCase().startsWith(input.toLowerCase())
        ).slice(0, 5);
        setOriginCitySuggestions(filteredSuggestions);
    } else {
        setOriginCitySuggestions([]);
    }
};

// format csv data results as required to be transferred into setGuestInformation
const updateGuestInformationCSV = (csvData) => {
  const newGuestInformation = csvData.results.data.map(row => ({
    name: `${row.city}, ${row.country}`,
    attendees: parseInt(row.number, 10)
  }));
  setguestInformation(currentGuestInfo => [...currentGuestInfo, ...newGuestInformation]);
}
// set city name and number of attendees to guestInformation array
const setGuestInformation = (city) => {
  const numAttendees = parseInt(attendees)
  setOriginCity(`${city.city}, ${city.country}`);
  const newOriginCity = {
    name: `${city.city}, ${city.country}`,
    attendees: numAttendees
  };
  setguestInformation([...guestInformation, newOriginCity]);
  setOriginCitySuggestions([]);
};


  // Calculator component code using ManualCarousel
  return (
    <div id="calculator" className="calculator-section">
      <ManualCarousel>
        {/* Slide 1 */}
        <div className="slide-content">
          <div className="calculator-title">
            <h1>Your Host Cities</h1>
            <p>Input up to 5 preferred cities for hosting your conference!</p>
          </div>
          <div className="notification-container">
          {fullListNotification && (<p className="list-notification">{fullListNotification}</p>)}
            <input
              type="text"
              placeholder={cityPlaceholder}
              value={cityInput}
              onChange={handleCityInputChange}
              onKeyDown={handleKeyDown}
              className="city-input"
            />
            {/* Autocomplete Suggestions */}
            {cityInput.length > 0 && suggestions.length > 0 && (
            <ul className="autocomplete-suggestions-one">
            {suggestions.map((suggestion, index) => (
            <li
              key={index}
              onClick={() => selectSuggestion(suggestion)}
              className={highlightedIndex === index ? "highlighted" : ""}
            >
              {suggestion.city}, {suggestion.country}
             </li>
            ))}
            </ul>
              ) }
          </div>

          {/* Preferred Cities Display */}
          <div className="preferred-cities-display">
            {transitions((style, city, _, index) => (
              <animated.div
                key={index}
                style={{ ...style, backgroundColor: city.color }}
                className="preferred-city"
              >
                {city.name}
                <button
                  onClick={() => handleRemoveCity(index)}
                  className="remove-city-button"
                >
                  &times;
                </button>
              </animated.div>
            ))}
          </div>
        </div>

        {/* Slide 2 */}
        <div className="slide-content">
          <div className="calculator-title">
            <h1>Your Attendees</h1>
            <p>Let us know who's joining and from where!</p>
          </div>
          <div className="content-container">  
          <div className="input-container"> 
          <div className="input-group">
            <input type="number" className="input-attendees" value={attendees} onChange={(e) => setAttendees(e.target.value)} placeholder=" # "/>
            <input type="text" className="input-origin" value={originCity} onChange={handleOriginCityChange} placeholder="Origin" />
            {originCity.length > 0 && originCitySuggestions.length > 0 && (
            <ul className="autocomplete-suggestions-two">
            {originCitySuggestions.map((city, index) => (
      <li key={index} onClick={() => setGuestInformation(city)}>
        {city.city}, {city.country}
      </li>
    ))}
  </ul>
)}
            <button className="addButton" onClick={handleAddGuestInfo}> Add </button>
          </div>
          {/* Your content for slide 2 */}
          <input id="browse-csv-button" type="file" accept=".csv" style={{display: 'none'}} onChange={handleFileUpload} />
          <p className="data-import-description">Already have data? Please upload it below!</p>
          <div className="button-group">
          <button onClick={() => document.getElementById('browse-csv-button').click()} className="importButton">Import Data CSV</button>

          {/* why is this ID upload-csv-button????????? */}
          <button id="Upload-CSV-button" className="calculateButton" onClick={handleCalculateEmissions}>Calculate</button> 
          </div>
          </div>
          <div className="results-container">
          {uploadResult && uploadResult.results && (
            <div>
          {uploadResult.results.data.map((row, index) => {
            // Determine the color for this row. Wrap the index if it exceeds the length of the colors array.
            const rowColor = colors[index % colors.length];
            return (
            <div key={index} className="data-row" style={{backgroundColor: rowColor}}>
              <span>{row.country}</span>
              <span>{row.city}</span>
              <span>{row.number}</span>
            </div>
          );
        })}
    </div>
  )}
</div>
          </div>
        </div>
      </ManualCarousel>
    </div>
  );
};

export default Calculator;

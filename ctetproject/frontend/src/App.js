import React from "react";
import "./App.css";
import Navbar from "./components/Navbar/Navbar";
import Home from "./components/Home/Home";
import Context from "./components/Context/Context";
import Calculator from "./components/Calculator/Calculator";
import Results from "./components/Results/Results";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";

function App() {
  return (
    <div className="App">
      <Navbar />

      <div className="snap-target">
        <Home />
      </div>

      <div className="snap-target">
        <Context />
      </div>

      <div className="snap-target">
        <Calculator />
      </div>

      <div className="snap-target">
        <Results />
      </div>
    </div>
  );
}

export default App;

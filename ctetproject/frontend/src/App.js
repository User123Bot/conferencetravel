import React from 'react';
import './App.css';
import Home from './components/Home';
import Context from './components/Context';
import Calculator from './components/Calculator';
import Results from './components/Results';

function App() {
  return (
    <div className="App">
      <Home />
      <Context />
      <Calculator />
      <Results />
    </div>
  );
}

export default App;

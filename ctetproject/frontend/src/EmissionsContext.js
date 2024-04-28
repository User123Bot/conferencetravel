// contexts/EmissionsContext.js
import React, { createContext, useState, useContext } from 'react';

const EmissionsContext = createContext();

export const useEmissions = () => useContext(EmissionsContext);

export const EmissionsProvider = ({ children }) => {
  const [emissionsData, setEmissionsData] = useState([]);

  return (
    <EmissionsContext.Provider value={{ emissionsData, setEmissionsData }}>
      {children}
    </EmissionsContext.Provider>
  );
};

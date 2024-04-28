// Navbar.js
import React from 'react';
import '../../App.css';
import './Navbar.css';

const Navbar = () => {
  const scrollToSection = (sectionId) => {
    const section = document.getElementById(sectionId);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (

    <div className="navbar">
      <span className='logo' onClick={() => scrollToSection('home')}>CTET</span>
      <span onClick={() => scrollToSection('home')}>Home</span>
      <span className='divider'>|</span>
      <span onClick={() => scrollToSection('context')}>About</span>
      <span className='divider'>|</span>
      <span onClick={() => scrollToSection('calculator')}>Calculator</span>
      <span className='divider'>|</span>
      <span onClick={() => scrollToSection('results')}>Results</span>
    </div>
  );
};

export default Navbar;

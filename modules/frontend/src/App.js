import React from 'react';
import './App.css';

import Persons from './components/Persons';

function App() {
  return (
    <div className="App">
      <div className="header">
        <h1>UdaConnect</h1>
      </div>
      <Persons />
    </div>
  );
}

export default App;

import React from "react";
import "./App.css";
import logo from "./images/UdaConnectLogo.svg";
import Persons from "./components/Persons";

function App() {
  return (
    <div className="App">
      <div className="header">
        <img src={logo} className="App-logo" alt="UdaConnect" />
      </div>
      <Persons />
    </div>
  );
}

export default App;

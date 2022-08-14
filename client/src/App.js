import logo from "./logo.svg";
import "./App.css";
import React, { useState } from "react";

function App() {
  const [res, setRes] = useState(null);

  const handleSend = () => {
    // Get the receiver endpoint from Python using fetch
    fetch("http://127.0.0.1:5000/receiver", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      // Stringify the payload into JSON
      body: JSON.stringify(cars),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          alert("something is wrong");
        }
      })
      .then((jsonResponse) => {
        // Log the response data in the console
        setRes(JSON.stringify(jsonResponse));
      })
      .catch((error) => console.log(error));
  };

  const handleStart = () => {
    fetch("http://127.0.0.1:5000/start", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          alert("something is wrong");
        }
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => console.log(error));
  };

  const cars = [
    { make: "Porsche", model: "911S" },
    { make: "Mercedez-Benz", model: "220SE" },
    { make: "Jaguar", model: "Mark VII" },
  ];

  const handleStop = () => {
    fetch("http://127.0.0.1:5000/end", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          alert("something is wrong");
        }
      })
      .then((response) => {
        alert(response);
      })
      .catch((error) => console.log(error));
  };

  const handleAccountInfo = () => {
    fetch("http://127.0.0.1:5000/account", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        } else {
          alert("something is wrong");
        }
      })
      .then((response) => {
        console.log(response);
      })
      .catch((error) => console.log(error));
  };

  return (
    <div>
      <h1>API Testing</h1>
      <body></body>
      <button id="send-button" onClick={handleSend}>
        Post to Python
      </button>
      <button onClick={handleStart}>Start Trading Bot</button>
      <button onClick={handleStop}>Stop Trading Bot</button>
      <button onClick={handleAccountInfo}>Get Account Info</button>
    </div>
  );
}

export default App;

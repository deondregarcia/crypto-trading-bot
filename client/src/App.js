import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect } from "react";
import CryptoDisplay from "./components/CryptoDisplay/CryptoDisplay";

function App() {
  const [res, setRes] = useState(null);
  const [balances, setBalances] = useState([]);
  const [botStatus, setBotStatus] = useState(false);

  const handleStart = () => {
    setBotStatus(true);
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

  const handleStop = () => {
    setBotStatus(false);
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

  // Coin balances to always display on screen even if balance == 0
  const alwaysDisplay = ["BTC", "ETH", "USD", "USDT", "DOGE"];
  const handleAccountInfo = async () => {
    await fetch("http://127.0.0.1:5000/account", {
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
        // console.log(response["balances"]);
        const resBalances = response["balances"].map((crypto, index) => crypto);
        const filteredRes = resBalances.filter((item) => {
          if (
            item.free != 0 ||
            item.locked != 0 ||
            alwaysDisplay.includes(item.asset)
          ) {
            return item;
          }
          // return item.free != 0;
        });
        // console.log("resBalances: " + resBalances);
        console.log(filteredRes);
        setBalances(filteredRes);
      })
      .catch((error) => console.log(error));
  };

  useEffect(() => {
    handleAccountInfo();

    return () => {};
  }, []);

  // console.log(balances.map((crypto, index) => crypto.asset));

  // {
  //   balanceState &&
  //     balances.map((balance, index) => {
  //       // <CryptoDisplay crypto={crypto} />;
  //       console.log(balance[0].asset);
  //     });
  // }

  // const crypto = {
  //   asset: "TEST",
  // };

  return (
    <div className="container">
      <h1 className="title">Cryptocurrency Trading Bot</h1>
      <div className="info-boxes-container">
        <div className="info-box">
          <h2>Balances</h2>
          <div className="info-box-content">
            {balances.map((balance, index) => (
              <CryptoDisplay crypto={balance} key={index} />
            ))}
          </div>
        </div>
        <div className="info-box">
          <h2>Trade History</h2>
          <div className="info-box-content"></div>
        </div>
        <div className="info-box">
          <h2>Statistics</h2>
          <div className="info-box-content">
            <p>Total P&amp;L: 0</p>
          </div>
        </div>
      </div>
      <div className="bot-info">
        <div className="bot-status">
          <h1>Bot Status:</h1>
          <h1>{botStatus ? "ON" : "OFF"}</h1>
        </div>
        <div className="bot-controls">
          <button onClick={handleStart}>Start Trading Bot</button>
          <button onClick={handleStop}>Stop Trading Bot</button>
          <button onClick={handleAccountInfo}>Get Account Info</button>
        </div>
      </div>
    </div>
  );
}

export default App;

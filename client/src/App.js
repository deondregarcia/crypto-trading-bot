import logo from "./logo.svg";
import "./App.css";
import React, { useState, useEffect } from "react";

// import components
import CryptoDisplay from "./components/CryptoDisplay/CryptoDisplay";
import Dropdown from "./components/Dropdown/Dropdown";
import HistoryDisplay from "./components/HistoryDisplay/HistoryDisplay";

function App() {
  const [res, setRes] = useState(null);
  const [balances, setBalances] = useState([]);
  const [botStatus, setBotStatus] = useState(false);
  const [coinHistory, setCoinHistory] = useState("Select Coin"); // state for Trade History dropdown
  const [historyDisplay, setHistoryDisplay] = useState(null);

  // start the bot
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

  // stop the bot
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
        const resBalances = response["balances"].map((crypto, index) => crypto);
        const filteredRes = resBalances.filter((item) => {
          if (
            item.free != 0 ||
            item.locked != 0 ||
            alwaysDisplay.includes(item.asset)
          ) {
            return item;
          }
        });
        setBalances(filteredRes);
      })
      .catch((error) => console.log(error));
  };

  const getTradeHistory = async () => {
    console.log(JSON.stringify(coinHistory));
    await fetch("http://127.0.0.1:5000/trade-history", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(coinHistory),
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
        setHistoryDisplay(response.reverse()); // reverse to display most recent order at the top
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const buyMarket = async () => {
    console.log(JSON.stringify(coinHistory));
    await fetch("http://127.0.0.1:5000/buy", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ symbol: "DOGEUSD", quantity: 350 }),
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
      .catch((error) => {
        console.log(error);
      });
  };

  // run once
  useEffect(() => {
    handleAccountInfo();

    return () => {};
  }, []);

  // run when changing trade history coin
  useEffect(() => {
    getTradeHistory();
    return () => {};
  }, [coinHistory]);

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
          <div className="info-box-content">
            <div className="history-dropdown-wrapper">
              <Dropdown
                setCoinHistory={setCoinHistory}
                coinHistory={coinHistory}
              />
            </div>
            <div>
              {historyDisplay ? (
                historyDisplay.map((order, index) => (
                  <HistoryDisplay order={order} index={index} />
                ))
              ) : (
                <p>Select Coin</p>
              )}
            </div>
          </div>
        </div>
        <div className="info-box">
          <h2>Statistics</h2>
          <div className="info-box-content">
            <p>Total P&amp;L: 0</p>
            {/* <button onClick={buyMarket}>Buy Market</button> */}
          </div>
        </div>
      </div>
      <div className="bot-info">
        <div className="bot-status">
          <h1>Bot Status:</h1>
          <h1>{botStatus ? "ON" : "OFF"}</h1>
        </div>
        <div className="bot-controls">
          <button onClick={handleStart} className="btn">
            Start Trading Bot
          </button>
          <button onClick={handleStop} className="btn">
            Stop Trading Bot
          </button>
          <button onClick={handleAccountInfo} className="btn">
            Get Account Info
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;

import React, { useState } from "react";
import "./Dropdown.css";

const Dropdown = (props) => {
  const [listState, setListState] = useState(false);

  const DropdownList = () => {
    return (
      <div className="dropdown-list" onClick={() => setListState(!listState)}>
        <div
          className="dropdown-list-btn"
          onClick={() => props.setCoinHistory("BTCUSD")}
        >
          BTCUSD
        </div>
        <div
          className="dropdown-list-btn"
          onClick={() => props.setCoinHistory("DOGEUSD")}
        >
          DOGEUSD
        </div>
        <div
          className="dropdown-list-btn"
          onClick={() => props.setCoinHistory("ETHUSD")}
        >
          ETHUSD
        </div>
      </div>
    );
  };

  return (
    <div className="box">
      <button className="dropdown-btn" onClick={() => setListState(!listState)}>
        {props.coinHistory}
      </button>
      {listState && <DropdownList />}
    </div>
  );
};

export default Dropdown;

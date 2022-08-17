import React from "react";

function CryptoDisplay({ crypto }) {
  return (
    <div>
      <p>Asset: {crypto.asset}</p>
      <p>Balance: {crypto.free}</p>
    </div>
  );
}

export default CryptoDisplay;

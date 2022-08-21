import React from "react";
import "./HistoryDisplay.css";

const HistoryDisplay = ({ order, index }) => {
  var orderDate = new Intl.DateTimeFormat("en-US", {
    dateStyle: "long",
    timeStyle: "long",
  }).format(order.time);
  return (
    <div className="history-display-container">
      <p>{index + 1}.</p>
      <p>{order.symbol}</p>
      <p>{orderDate}</p>
      <p>Price: {order.price}</p>
      <p>Quantity: {order.qty}</p>
      <p>Quote Quantity: {order.quoteQty}</p>
    </div>
  );
};

export default HistoryDisplay;

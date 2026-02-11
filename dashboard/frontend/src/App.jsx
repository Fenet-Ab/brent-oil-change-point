import React, { useEffect, useState } from "react";
import PriceChart from "./components/PriceChart";

function App() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/prices")
      .then((res) => res.json())
      .then((json) => setData(json));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Brent Oil Prices & Change Point Analysis</h2>

      <PriceChart
        data={data}
        changePointDate="2020-03-15"
      />
    </div>
  );
}

export default App;

import React, { useEffect, useState } from "react";
import PriceChart from "./components/PriceChart";
import EventList from "./components/EventList";
import MetricsPanel from "./components/MetricsPanel";
import "./App.css";

const API_BASE_URL = "http://localhost:5000";

function App() {
  const [priceData, setPriceData] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [events, setEvents] = useState([]);
  const [associations, setAssociations] = useState([]);
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [dateRange, setDateRange] = useState({
    start: "1987-05-20",
    end: "2022-09-30"
  });

  // Fetch all data
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Fetch prices
        const pricesRes = await fetch(
          `${API_BASE_URL}/prices?start_date=${dateRange.start}&end_date=${dateRange.end}`
        );
        const pricesJson = await pricesRes.json();
        if (pricesJson.status === "success") {
          setPriceData(pricesJson.data);
        }

        // Fetch change points
        const cpRes = await fetch(`${API_BASE_URL}/changepoints`);
        const cpJson = await cpRes.json();
        if (cpJson.status === "success") {
          setChangePoints(cpJson.data);
        }

        // Fetch events
        const eventsRes = await fetch(
          `${API_BASE_URL}/events?start_date=${dateRange.start}&end_date=${dateRange.end}`
        );
        const eventsJson = await eventsRes.json();
        if (eventsJson.status === "success") {
          setEvents(eventsJson.data);
        }

        // Fetch associations
        const assocRes = await fetch(`${API_BASE_URL}/associations?window_days=30`);
        const assocJson = await assocRes.json();
        if (assocJson.status === "success") {
          setAssociations(assocJson.data);
        }

        // Fetch metrics
        const metricsRes = await fetch(`${API_BASE_URL}/metrics`);
        const metricsJson = await metricsRes.json();
        if (metricsJson.status === "success") {
          setMetrics(metricsJson);
        }

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchData();
  }, [dateRange]);

  const handleEventSelect = (event) => {
    setSelectedEvent(event);
  };

  const handleDateRangeChange = (newRange) => {
    setDateRange(newRange);
  };

  if (loading) {
    return (
      <div className="app-container">
        <div className="loading">Loading data...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error">Error: {error}</div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Brent Oil Price Change Point Analysis</h1>
        <p className="subtitle">
          Detecting structural breaks and associating them with geopolitical events
        </p>
      </header>

      <div className="main-content">
        <div className="left-panel">
          <MetricsPanel metrics={metrics} />
          <EventList
            events={events}
            associations={associations}
            onEventSelect={handleEventSelect}
            selectedEvent={selectedEvent}
          />
        </div>

        <div className="right-panel">
          <PriceChart
            data={priceData}
            changePoints={changePoints}
            events={events}
            selectedEvent={selectedEvent}
            dateRange={dateRange}
            onDateRangeChange={handleDateRangeChange}
          />
        </div>
      </div>
    </div>
  );
}

export default App;

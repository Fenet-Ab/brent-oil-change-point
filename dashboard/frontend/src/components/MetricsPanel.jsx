import React from "react";
import "./MetricsPanel.css";

const MetricsPanel = ({ metrics }) => {
  if (!metrics) {
    return (
      <div className="metrics-panel">
        <h2>Key Metrics</h2>
        <p>Loading...</p>
      </div>
    );
  }

  const { price_statistics, returns_statistics, volatility_statistics, date_range } = metrics;

  return (
    <div className="metrics-panel">
      <h2>Key Metrics</h2>

      <div className="metric-section">
        <h3>Price Statistics</h3>
        <div className="metric-grid">
          <div className="metric-item">
            <span className="metric-label">Mean Price</span>
            <span className="metric-value">${price_statistics?.mean?.toFixed(2)}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Min Price</span>
            <span className="metric-value">${price_statistics?.min?.toFixed(2)}</span>
            <span className="metric-date">{price_statistics?.min_date}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Max Price</span>
            <span className="metric-value">${price_statistics?.max?.toFixed(2)}</span>
            <span className="metric-date">{price_statistics?.max_date}</span>
          </div>
        </div>
      </div>

      <div className="metric-section">
        <h3>Returns Statistics</h3>
        <div className="metric-grid">
          <div className="metric-item">
            <span className="metric-label">Mean Return</span>
            <span className="metric-value">
              {(returns_statistics?.mean * 100)?.toFixed(4)}%
            </span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Volatility (Std)</span>
            <span className="metric-value">
              {(returns_statistics?.std * 100)?.toFixed(4)}%
            </span>
          </div>
        </div>
      </div>

      <div className="metric-section">
        <h3>Volatility</h3>
        <div className="metric-grid">
          <div className="metric-item">
            <span className="metric-label">Mean 30-Day Vol</span>
            <span className="metric-value">
              {(volatility_statistics?.mean_30day * 100)?.toFixed(4)}%
            </span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Max 30-Day Vol</span>
            <span className="metric-value">
              {(volatility_statistics?.max_30day * 100)?.toFixed(4)}%
            </span>
            <span className="metric-date">{volatility_statistics?.max_vol_date}</span>
          </div>
        </div>
      </div>

      <div className="metric-section">
        <h3>Data Coverage</h3>
        <div className="metric-grid">
          <div className="metric-item">
            <span className="metric-label">Observations</span>
            <span className="metric-value">{date_range?.total_observations?.toLocaleString()}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Total Days</span>
            <span className="metric-value">{date_range?.total_days?.toLocaleString()}</span>
          </div>
          <div className="metric-item">
            <span className="metric-label">Date Range</span>
            <span className="metric-value-small">
              {date_range?.start} to {date_range?.end}
            </span>
          </div>
        </div>
      </div>

      <div className="metric-section">
        <h3>Events</h3>
        <div className="metric-item">
          <span className="metric-label">Total Events</span>
          <span className="metric-value">{metrics?.total_events}</span>
        </div>
      </div>
    </div>
  );
};

export default MetricsPanel;


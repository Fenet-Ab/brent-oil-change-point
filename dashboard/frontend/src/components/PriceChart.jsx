import React, { useMemo } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
  Legend,
} from "recharts";

const PriceChart = ({
  data,
  changePoints = [],
  events = [],
  selectedEvent = null,
  dateRange,
  onDateRangeChange,
}) => {
  // Prepare data for chart
  const chartData = useMemo(() => {
    return data.map((item) => {
      const itemDate = item.Date;
      
      // Check if this date has an event
      const eventOnDate = events.find(
        (e) => e.Date === itemDate
      );
      
      return {
        Date: itemDate,
        Price: parseFloat(item.Price) || 0,
        logReturn: item.log_return ? parseFloat(item.log_return) : null,
        hasEvent: !!eventOnDate,
        event: eventOnDate?.Event || null,
        isSelectedEvent: selectedEvent && selectedEvent.Date === itemDate,
      };
    });
  }, [data, events, selectedEvent]);

  // Format date for display
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    });
  };

  // Custom tooltip
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div
          style={{
            backgroundColor: "white",
            border: "1px solid #ccc",
            padding: "12px",
            borderRadius: "6px",
            boxShadow: "0 2px 8px rgba(0,0,0,0.15)",
          }}
        >
          <p style={{ fontWeight: "bold", marginBottom: "8px" }}>
            {formatDate(label)}
          </p>
          <p style={{ color: "#2563eb" }}>
            <strong>Price:</strong> ${data.Price.toFixed(2)} per barrel
          </p>
          {data.event && (
            <p style={{ color: "#dc2626", marginTop: "8px" }}>
              <strong>Event:</strong> {data.event}
            </p>
          )}
          {data.logReturn !== null && (
            <p style={{ color: "#6b7280", fontSize: "0.9em", marginTop: "4px" }}>
              Log Return: {data.logReturn.toFixed(4)}
            </p>
          )}
        </div>
      );
    }
    return null;
  };

  return (
    <div>
      <div style={{ marginBottom: "20px" }}>
        <h2 style={{ color: "#1e40af", marginBottom: "10px" }}>
          Historical Brent Oil Prices
        </h2>
        <div style={{ display: "flex", gap: "10px", marginBottom: "15px" }}>
          <input
            type="date"
            value={dateRange.start}
            onChange={(e) =>
              onDateRangeChange({ ...dateRange, start: e.target.value })
            }
            style={{
              padding: "8px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
          <span style={{ alignSelf: "center" }}>to</span>
          <input
            type="date"
            value={dateRange.end}
            onChange={(e) =>
              onDateRangeChange({ ...dateRange, end: e.target.value })
            }
            style={{
              padding: "8px",
              border: "1px solid #ccc",
              borderRadius: "4px",
            }}
          />
        </div>
      </div>

      <ResponsiveContainer width="100%" height={500}>
        <LineChart
          data={chartData}
          margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="Date"
            tick={{ fontSize: 12 }}
            tickFormatter={(value) => {
              const date = new Date(value);
              return date.toLocaleDateString("en-US", {
                year: "numeric",
                month: "short",
              });
            }}
            minTickGap={50}
          />
          <YAxis
            domain={["auto", "auto"]}
            tick={{ fontSize: 12 }}
            label={{
              value: "USD per barrel",
              angle: -90,
              position: "insideLeft",
              style: { textAnchor: "middle" },
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend />

          {/* Main price line */}
          <Line
            type="monotone"
            dataKey="Price"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
            name="Brent Oil Price"
          />

          {/* Change point reference lines */}
          {changePoints.map((cp, idx) => (
            <ReferenceLine
              key={`cp-${idx}`}
              x={cp.date}
              stroke="#dc2626"
              strokeDasharray="4 4"
              strokeWidth={2}
              label={{
                value: `Change Point: ${cp.date}`,
                position: "top",
                fill: "#dc2626",
                fontSize: 11,
              }}
            />
          ))}

          {/* Selected event reference line */}
          {selectedEvent && (
            <ReferenceLine
              x={selectedEvent.Date}
              stroke="#16a34a"
              strokeDasharray="2 2"
              strokeWidth={2}
              label={{
                value: selectedEvent.Event,
                position: "top",
                fill: "#16a34a",
                fontSize: 11,
              }}
            />
          )}
        </LineChart>
      </ResponsiveContainer>

      {/* Change points info */}
      {changePoints.length > 0 && (
        <div style={{ marginTop: "20px", padding: "15px", background: "#f9fafb", borderRadius: "6px" }}>
          <h3 style={{ fontSize: "1rem", marginBottom: "10px", color: "#374151" }}>
            Detected Change Points:
          </h3>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))", gap: "10px" }}>
            {changePoints.map((cp, idx) => (
              <div
                key={idx}
                style={{
                  padding: "10px",
                  background: "white",
                  borderRadius: "4px",
                  border: "1px solid #e5e7eb",
                }}
              >
                <div style={{ fontWeight: "bold", color: "#dc2626" }}>
                  {cp.date}
                </div>
                <div style={{ fontSize: "0.85em", color: "#6b7280", marginTop: "4px" }}>
                  Impact: {cp.impact_pct?.toFixed(2)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceChart;

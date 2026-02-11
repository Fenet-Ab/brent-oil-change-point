import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ReferenceLine,
  ResponsiveContainer,
} from "recharts";

/**
 * Props:
 *  - data: [{ Date, Price, event }]
 *  - changePointDate: "2020-03-15"
 */
const PriceChart = ({ data, changePointDate }) => {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
        <CartesianGrid strokeDasharray="3 3" />

        <XAxis
          dataKey="Date"
          tick={{ fontSize: 12 }}
          minTickGap={50}
        />

        <YAxis
          domain={["auto", "auto"]}
          tick={{ fontSize: 12 }}
          label={{ value: "USD per barrel", angle: -90, position: "insideLeft" }}
        />

        <Tooltip content={<CustomTooltip />} />

        {/* Brent Price Line */}
        <Line
          type="monotone"
          dataKey="Price"
          stroke="#2563eb"
          dot={false}
          strokeWidth={2}
        />

        {/* Change Point Vertical Line */}
        <ReferenceLine
          x={changePointDate}
          stroke="red"
          strokeDasharray="4 4"
          label={{ value: "Change Point", position: "top", fill: "red" }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default PriceChart;

/* -------------------------------
   Custom Tooltip
--------------------------------*/
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const price = payload[0].value;
    const event = payload[0].payload.event;

    return (
      <div
        style={{
          backgroundColor: "white",
          border: "1px solid #ccc",
          padding: "10px",
          borderRadius: "6px",
        }}
      >
        <p><strong>Date:</strong> {label}</p>
        <p><strong>Price:</strong> ${price.toFixed(2)}</p>
        {event && <p><strong>Event:</strong> {event}</p>}
      </div>
    );
  }
  return null;
};

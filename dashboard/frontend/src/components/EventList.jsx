import React from "react";
import "./EventList.css";

const EventList = ({ events, associations, onEventSelect, selectedEvent }) => {
  // Group events by decade for better organization
  const eventsByDecade = events.reduce((acc, event) => {
    const year = new Date(event.Date).getFullYear();
    const decade = Math.floor(year / 10) * 10;
    if (!acc[decade]) acc[decade] = [];
    acc[decade].push(event);
    return acc;
  }, {});

  return (
    <div className="event-list-container">
      <h2>Key Events</h2>
      <p className="event-list-subtitle">
        Click an event to highlight it on the chart
      </p>

      <div className="event-list">
        {Object.keys(eventsByDecade)
          .sort((a, b) => b - a)
          .map((decade) => (
            <div key={decade} className="decade-group">
              <h3 className="decade-header">{decade}s</h3>
              {eventsByDecade[decade].map((event, idx) => {
                const isSelected = selectedEvent?.Date === event.Date;
                const hasAssociation = associations.some(
                  (a) => a.event_date === event.Date
                );

                return (
                  <div
                    key={idx}
                    className={`event-item ${isSelected ? "selected" : ""} ${
                      hasAssociation ? "has-association" : ""
                    }`}
                    onClick={() => onEventSelect(event)}
                  >
                    <div className="event-date">
                      {new Date(event.Date).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "short",
                        day: "numeric",
                      })}
                    </div>
                    <div className="event-name">{event.Event}</div>
                    {event.Description && (
                      <div className="event-description">
                        {event.Description.substring(0, 100)}
                        {event.Description.length > 100 ? "..." : ""}
                      </div>
                    )}
                    {hasAssociation && (
                      <div className="association-badge">Linked to Change Point</div>
                    )}
                  </div>
                );
              })}
            </div>
          ))}
      </div>
    </div>
  );
};

export default EventList;


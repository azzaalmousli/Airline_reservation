const STATUS_CLASS = {
  Scheduled: 'badge-info',
  Delayed:   'badge-warning',
  Arrived:   'badge-success',
  Departed:  'badge-neutral',
  Canceled:  'badge-danger',
};

function fmtTime(dt) {
  return new Date(dt).toLocaleTimeString('en-US', {
    timeZone: 'UTC', hour: '2-digit', minute: '2-digit',
  });
}

export default function FlightCard({ flight, onBook }) {
  const dep         = fmtTime(flight.departure_time);
  const arr         = fmtTime(flight.arrival_time);
  const statusClass = STATUS_CLASS[flight.status] || 'badge-neutral';

  return (
    <div className="flight-card">
      {/* Route codes */}
      <div style={{ minWidth: 120 }}>
        <div className="flight-route-codes">
          <span>{flight.departure_iata}</span>
          <span className="flight-arrow">→</span>
          <span>{flight.arrival_iata}</span>
        </div>
        <div className="flight-cities">
          {flight.departure_city} → {flight.arrival_city}
        </div>
      </div>

      {/* Departure */}
      <div className="flight-time-block">
        <div className="flight-time-value">{dep}</div>
        <div className="flight-time-label">Departs</div>
      </div>

      {/* Duration line */}
      <div className="flight-duration-line" style={{ flex: 1, fontSize: '0.68rem', color: 'var(--text-3)' }}>
        {flight.model}
      </div>

      {/* Arrival */}
      <div className="flight-time-block">
        <div className="flight-time-value">{arr}</div>
        <div className="flight-time-label">Arrives</div>
      </div>

      {/* Status + meta */}
      <div className="flight-meta-col">
        <span className={`badge ${statusClass}`}>{flight.status}</span>
        {flight.load_factor_pct != null && (
          <span className="flight-sub">{flight.load_factor_pct.toFixed(1)}% full</span>
        )}
      </div>

      {/* Price + CTA */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.4rem' }}>
        <div className="flight-price">$300</div>
        <button
          className="btn btn-primary btn-sm"
          onClick={() => onBook(flight.flight_number)}
        >
          Book
        </button>
      </div>
    </div>
  );
}

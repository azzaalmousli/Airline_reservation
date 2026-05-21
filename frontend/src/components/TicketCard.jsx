export default function TicketCard({ ticket, onPay, onCancel }) {
  const raw       = (ticket.payment_status || '').toLowerCase();
  const isUnpaid  = raw === 'unpaid';
  const isPartial = raw === 'partial';

  const badgeClass = isUnpaid  ? 'badge-danger'
                   : isPartial ? 'badge-warning'
                               : 'badge-success';

  const payLabel   = isUnpaid ? 'Unpaid' : isPartial ? 'Partial' : 'Paid';

  return (
    <div className="ticket-card">
      {/* Left: flight info */}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div className="ticket-flight-num">
          {ticket.flight_number} &bull; Seat {ticket.seat_number}
        </div>
        <div className="ticket-route">
          {ticket.departure_airport} → {ticket.arrival_airport}
        </div>
        <div className="ticket-meta">
          {ticket.fare_class} &bull; {ticket.passenger_type} &bull; Booking #{ticket.booking_id}
        </div>
      </div>

      {/* Right: price, status, actions */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem', flexShrink: 0 }}>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '1.05rem', fontWeight: 700 }}>${ticket.price}</div>
          <span className={`badge ${badgeClass}`}>{payLabel}</span>
        </div>

        <div style={{ display: 'flex', gap: '0.5rem' }}>
          {isUnpaid && (
            <button
              className="btn btn-success btn-sm"
              onClick={() => onPay(ticket.ticket_number, ticket.price)}
            >
              Pay
            </button>
          )}
          <button
            className="btn btn-danger btn-sm"
            onClick={() => onCancel(ticket.ticket_number)}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

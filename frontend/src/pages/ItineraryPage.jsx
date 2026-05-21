import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import TicketCard from '../components/TicketCard';
import PaymentModal from '../components/PaymentModal';

export default function ItineraryPage() {
  const [tickets,  setTickets]  = useState([]);
  const [loading,  setLoading]  = useState(true);
  const [error,    setError]    = useState('');
  const [payment,  setPayment]  = useState(null); // { ticket, amount }

  const { user }  = useAuth();
  const navigate  = useNavigate();

  const fetchItinerary = useCallback(async () => {
    if (!user) return;
    setLoading(true);
    setError('');
    try {
      const data = await api.getItinerary(user.id);
      if (data.status === 'success') {
        setTickets(data.data ?? []);
      } else {
        setError(data.message || 'Failed to load itinerary.');
      }
    } catch {
      setError('Cannot reach the server.');
    } finally {
      setLoading(false);
    }
  }, [user]);

  useEffect(() => {
    if (!user) { navigate('/login'); return; }
    fetchItinerary();
  }, [user, navigate, fetchItinerary]);

  const handleCancel = async (ticketNumber) => {
    if (!window.confirm(`Cancel ticket #${ticketNumber}? This cannot be undone.`)) return;
    try {
      const data = await api.cancelTicket(ticketNumber);
      if (data.status === 'success') {
        fetchItinerary();
      } else {
        alert('Cancellation failed: ' + data.message);
      }
    } catch {
      alert('Cannot connect to the server.');
    }
  };

  if (!user) return null;

  const unpaidCount = tickets.filter((t) => (t.payment_status || '').toLowerCase() === 'unpaid').length;
  const paidCount   = tickets.length - unpaidCount;

  return (
    <div className="page-enter">
      <div className="page-header">
        <h1 className="page-title">{user.name}'s Itinerary</h1>
        <p className="page-subtitle">Manage your reservations and payments</p>
      </div>

      {/* Stats */}
      {tickets.length > 0 && (
        <div className="stats-row">
          <div className="stat-card">
            <div className="stat-value">{tickets.length}</div>
            <div className="stat-label">Bookings</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--danger)' }}>{unpaidCount}</div>
            <div className="stat-label">Unpaid</div>
          </div>
          <div className="stat-card">
            <div className="stat-value" style={{ color: 'var(--success)' }}>{paidCount}</div>
            <div className="stat-label">Confirmed</div>
          </div>
        </div>
      )}

      {loading && <div className="spinner" />}

      {!loading && error && (
        <div className="alert alert-error">{error}</div>
      )}

      {!loading && !error && tickets.length === 0 && (
        <div className="empty-state card">
          <div className="empty-state-icon">✈</div>
          <div className="empty-state-title">No bookings yet</div>
          <div className="empty-state-text">
            Head to Search Flights to reserve your first seat.
          </div>
        </div>
      )}

      {!loading && tickets.length > 0 && (
        <div className="ticket-list">
          {tickets.map((t) => (
            <TicketCard
              key={t.ticket_number}
              ticket={t}
              onPay={(tn, amt) => setPayment({ ticket: tn, amount: amt })}
              onCancel={handleCancel}
            />
          ))}
        </div>
      )}

      {/* Payment modal – rendered in-place, no navigation required */}
      {payment && (
        <PaymentModal
          ticket={payment.ticket}
          amount={payment.amount}
          onSuccess={() => { setPayment(null); fetchItinerary(); }}
          onClose={() => setPayment(null)}
        />
      )}
    </div>
  );
}

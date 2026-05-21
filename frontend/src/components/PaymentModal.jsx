import { useState } from 'react';
import { api } from '../api/client';

export default function PaymentModal({ ticket, amount, onSuccess, onClose }) {
  const [name,    setName]    = useState('');
  const [number,  setNumber]  = useState('');
  const [expiry,  setExpiry]  = useState('');
  const [cvv,     setCvv]     = useState('');
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  // Format card number with spaces every 4 digits
  const handleNumberChange = (e) => {
    const digits = e.target.value.replace(/\D/g, '').slice(0, 16);
    setNumber(digits.replace(/(.{4})/g, '$1 ').trim());
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim() || !number.trim() || !expiry.trim() || !cvv.trim()) {
      setError('Please complete all card fields.');
      return;
    }
    setLoading(true);
    setError('');

    try {
      const data = await api.processPayment(ticket, parseFloat(amount));
      if (data.status === 'success') {
        onSuccess();
      } else {
        setError(data.message || 'Payment failed. Please try again.');
      }
    } catch {
      setError('Cannot reach the payment server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="modal-overlay"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="modal">
        <div className="modal-title">
          <span style={{ color: 'var(--success)' }}>⚿</span> Secure Checkout
        </div>

        {/* Amount summary */}
        <div style={{
          background:    'var(--primary-dim)',
          border:        '1px solid rgba(56,189,248,0.2)',
          borderRadius:  'var(--radius-sm)',
          padding:       '0.75rem 1rem',
          marginBottom:  '1.5rem',
          display:       'flex',
          justifyContent:'space-between',
          alignItems:    'center',
        }}>
          <span style={{ fontSize: '0.82rem', color: 'var(--text-2)' }}>
            Ticket #{ticket}
          </span>
          <span style={{ fontSize: '1.35rem', fontWeight: 700, color: 'var(--primary)' }}>
            ${amount}
          </span>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Cardholder Name</label>
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Name on card"
              autoFocus
            />
          </div>

          <div className="form-group">
            <label>Card Number</label>
            <input
              value={number}
              onChange={handleNumberChange}
              placeholder="0000 0000 0000 0000"
              maxLength={19}
              style={{ letterSpacing: '0.1em' }}
            />
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label>Expiry (MM/YY)</label>
              <input
                value={expiry}
                onChange={(e) => setExpiry(e.target.value)}
                placeholder="MM/YY"
                maxLength={5}
              />
            </div>
            <div className="form-group">
              <label>CVV</label>
              <input
                type="password"
                value={cvv}
                onChange={(e) => setCvv(e.target.value)}
                placeholder="•••"
                maxLength={3}
              />
            </div>
          </div>

          {error && <div className="alert alert-error">{error}</div>}

          <button
            type="submit"
            className="btn btn-success btn-full"
            disabled={loading}
          >
            {loading ? 'Processing…' : `Confirm Payment — $${amount}`}
          </button>
          <button
            type="button"
            className="btn btn-outline btn-full"
            onClick={onClose}
            disabled={loading}
          >
            Cancel
          </button>
        </form>
      </div>
    </div>
  );
}

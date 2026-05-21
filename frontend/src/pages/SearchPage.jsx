import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';
import FlightCard from '../components/FlightCard';

export default function SearchPage() {
  const [from,     setFrom]     = useState('');
  const [to,       setTo]       = useState('');
  const [date,     setDate]     = useState('');
  const [flights,  setFlights]  = useState([]);
  const [loading,  setLoading]  = useState(false);
  const [error,    setError]    = useState('');
  const [searched, setSearched] = useState(false);

  const { user } = useAuth();
  const navigate = useNavigate();

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!from.trim() || !to.trim() || !date) {
      setError('Please fill in all three fields.');
      return;
    }
    setLoading(true);
    setError('');
    setSearched(false);

    try {
      const data = await api.searchFlights(from.trim().toUpperCase(), to.trim().toUpperCase(), date);
      if (data.status === 'success') {
        setFlights(data.data ?? []);
        setSearched(true);
      } else {
        setError(data.message || 'Search failed.');
      }
    } catch {
      setError('Cannot reach the server — is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleBook = async (flightNumber) => {
    if (!user) {
      navigate('/login');
      return;
    }
    if (!window.confirm(`Reserve a seat on flight ${flightNumber}?`)) return;

    try {
      const data = await api.bookFlight(user.id, flightNumber);
      if (data.status === 'success') {
        navigate('/itinerary');
      } else {
        alert('Booking failed: ' + data.message);
      }
    } catch {
      alert('Cannot connect to the server.');
    }
  };

  return (
    <div className="page-enter">
      <div className="page-header">
        <h1 className="page-title">Find Your Flight</h1>
        <p className="page-subtitle">Search across all AeroSmart routes worldwide</p>
      </div>

      {/* Search form */}
      <form onSubmit={handleSearch} className="search-form">
        <div className="form-group">
          <label>From</label>
          <input
            value={from}
            onChange={(e) => setFrom(e.target.value)}
            placeholder="IST"
            maxLength={3}
            style={{ textTransform: 'uppercase' }}
          />
        </div>
        <div className="form-group">
          <label>To</label>
          <input
            value={to}
            onChange={(e) => setTo(e.target.value)}
            placeholder="LHR"
            maxLength={3}
            style={{ textTransform: 'uppercase' }}
          />
        </div>
        <div className="form-group">
          <label>Departure Date</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>
        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? '…' : 'Search'}
        </button>
      </form>

      {error && (
        <div className="alert alert-error" style={{ marginTop: '1rem' }}>{error}</div>
      )}

      {loading && <div className="spinner" />}

      {searched && !loading && (
        <div className="flight-grid">
          {flights.length === 0 ? (
            <div className="empty-state card">
              <div className="empty-state-icon">✈</div>
              <div className="empty-state-title">No flights found</div>
              <div className="empty-state-text">
                Try a different route or date. Remember to use IATA codes (e.g. IST, LHR, DXB).
              </div>
            </div>
          ) : (
            <>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-2)', marginBottom: '0.25rem' }}>
                {flights.length} flight{flights.length !== 1 ? 's' : ''} found
              </p>
              {flights.map((f) => (
                <FlightCard key={f.flight_number} flight={f} onBook={handleBook} />
              ))}
            </>
          )}
        </div>
      )}
    </div>
  );
}

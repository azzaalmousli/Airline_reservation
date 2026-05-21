import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../api/client';

const EMPTY = { name: '', email: '', passport: '', dob: '', phone: '' };

export default function RegisterPage() {
  const [form,    setForm]    = useState(EMPTY);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState('');

  const { login } = useAuth();
  const navigate  = useNavigate();

  const set = (field) => (e) => setForm((prev) => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (Object.values(form).some((v) => !v.trim())) {
      setError('All fields are required.');
      return;
    }
    setLoading(true);
    setError('');

    try {
      const data = await api.register(form);
      if (data.status === 'success') {
        login(data.user);
        navigate('/search');
      } else {
        setError(data.message || 'Registration failed.');
      }
    } catch {
      setError('Cannot connect to the server.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page page-enter">
      <div className="auth-card" style={{ maxWidth: 440 }}>
        <h2 className="auth-card-title">Create account</h2>
        <p className="auth-card-sub">Join AeroSmart Airlines today</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="form-group">
            <label>Full Name</label>
            <input value={form.name} onChange={set('name')} placeholder="Your full name" autoFocus />
          </div>

          <div className="form-group">
            <label>Email Address</label>
            <input type="email" value={form.email} onChange={set('email')} placeholder="you@example.com" />
          </div>

          <div className="grid-2">
            <div className="form-group">
              <label>Passport Number</label>
              <input value={form.passport} onChange={set('passport')} placeholder="P12345678" />
            </div>
            <div className="form-group">
              <label>Date of Birth</label>
              <input type="date" value={form.dob} onChange={set('dob')} />
            </div>
          </div>

          <div className="form-group">
            <label>Phone Number</label>
            <input value={form.phone} onChange={set('phone')} placeholder="+90 555 123 4567" />
          </div>

          {error && <div className="alert alert-error">{error}</div>}

          <button className="btn btn-primary btn-full" type="submit" disabled={loading}>
            {loading ? 'Creating account…' : 'Create Account'}
          </button>
        </form>

        <div className="auth-footer">
          Already have an account? <Link to="/login">Sign in</Link>
        </div>
      </div>
    </div>
  );
}

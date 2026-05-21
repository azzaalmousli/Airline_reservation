import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import AIAssistant from './AIAssistant';

const NAV_MAIN = [
  { to: '/search',    icon: '✈',  label: 'Search Flights' },
  { to: '/itinerary', icon: '≡',  label: 'My Itinerary'   },
];

const NAV_ACCOUNT = [
  { to: '/login',    icon: '→',  label: 'Sign In'  },
  { to: '/register', icon: '+',  label: 'Register' },
];

export default function Sidebar() {
  const { user, logout } = useAuth();
  const navigate         = useNavigate();

  return (
    <nav className="sidebar">
      {/* ── Logo ── */}
      <div className="sidebar-logo">
        <div className="sidebar-logo-icon">✈</div>
        <span className="sidebar-logo-text">AeroSmart</span>
        <span className="sidebar-logo-version">v2</span>
      </div>

      <div className="sidebar-divider" />

      {/* ── Main nav ── */}
      <span className="sidebar-section-label">Navigation</span>
      {NAV_MAIN.map(({ to, icon, label }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
        >
          <span className="nav-icon">{icon}</span>
          {label}
        </NavLink>
      ))}

      {/* ── Account nav (only when logged out) ── */}
      {!user && (
        <>
          <div className="sidebar-divider" style={{ marginTop: '0.5rem' }} />
          <span className="sidebar-section-label">Account</span>
          {NAV_ACCOUNT.map(({ to, icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              <span className="nav-icon">{icon}</span>
              {label}
            </NavLink>
          ))}
        </>
      )}

      {/* ── Spacer pushes AI + user card to bottom ── */}
      <div className="sidebar-spacer" />

      {/* ── AI assistant ── */}
      <AIAssistant />

      {/* ── User card ── */}
      {user ? (
        <div className="user-card">
          <div className="user-card-name">
            <span>◉</span> {user.name}
          </div>
          <div className="user-card-sub">Passenger ID #{user.id}</div>
          <button
            className="btn btn-danger btn-sm btn-full"
            onClick={() => { logout(); navigate('/login'); }}
          >
            Sign Out
          </button>
        </div>
      ) : (
        <div className="user-card">
          <div className="user-card-sub" style={{ marginBottom: 0 }}>Not signed in</div>
          <button
            className="btn btn-primary btn-sm btn-full"
            style={{ marginTop: '0.5rem' }}
            onClick={() => navigate('/login')}
          >
            Sign In
          </button>
        </div>
      )}
    </nav>
  );
}

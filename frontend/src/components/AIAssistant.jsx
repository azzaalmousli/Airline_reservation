import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api/client';

export default function AIAssistant() {
  const [input,    setInput]    = useState('');
  const [response, setResponse] = useState('');
  const [loading,  setLoading]  = useState(false);
  const navigate                = useNavigate();

  const ask = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setResponse('');

    try {
      const data = await api.getIntent(input.trim());

      switch (data.action) {
        case 'route_to_search':
          navigate('/search');
          setResponse('Opening flight search.');
          break;
        case 'route_to_login':
          navigate('/login');
          setResponse('Taking you to sign in.');
          break;
        case 'route_to_itinerary':
          navigate('/itinerary');
          setResponse('Loading your bookings.');
          break;
        default:
          setResponse("I didn't understand that. Try: \"book a flight\" or \"show my itinerary\".");
      }
      setInput('');
    } catch {
      setResponse('AI service unavailable.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ai-widget">
      <div className="ai-title">
        <div className="ai-pulse" />
        AI Assistant
      </div>

      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && ask()}
        placeholder="Ask me anything…"
        disabled={loading}
        style={{ marginBottom: '0.5rem' }}
      />

      <button
        className="btn btn-primary btn-sm btn-full"
        onClick={ask}
        disabled={loading || !input.trim()}
      >
        {loading ? '…' : 'Ask'}
      </button>

      {response && <div className="ai-response">{response}</div>}
    </div>
  );
}

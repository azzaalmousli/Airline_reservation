// Dev: VITE_API_URL is unset → BASE = '/api' → Vite proxy forwards to Flask:5000
// Prod (Vercel): VITE_API_URL = 'https://your-app.up.railway.app' → direct call
const BASE = (import.meta.env.VITE_API_URL ?? '') + '/api';

async function req(path, options = {}) {
  const { body, ...rest } = options;
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...rest,
    ...(body !== undefined ? { body: JSON.stringify(body) } : {}),
  });
  return res.json();
}

export const api = {
  // Auth
  login:    (email) => req('/auth/login',    { method: 'POST', body: { email } }),
  register: (data)  => req('/auth/register', { method: 'POST', body: data }),

  // Flights
  searchFlights: (from, to, date) => req(`/flights?from=${from}&to=${to}&date=${date}`),

  // Reservations
  bookFlight: (customerId, flightNumber) =>
    req('/reservations', { method: 'POST', body: { customer_id: customerId, flight_number: flightNumber } }),

  getItinerary: (customerId) => req(`/itinerary/${customerId}`),

  // Payment
  processPayment: (ticketNumber, amount) =>
    req('/payments', { method: 'POST', body: { ticket_number: ticketNumber, amount } }),

  // Cancel
  cancelTicket: (ticketNumber) =>
    req('/tickets/cancel', { method: 'POST', body: { ticket_number: ticketNumber } }),

  // AI
  getIntent: (message) => req('/ai/intent', { method: 'POST', body: { message } }),
};

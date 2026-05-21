// All paths are relative — Vite's proxy rewrites /api/* → http://127.0.0.1:5000/api/*
const BASE = '/api';

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

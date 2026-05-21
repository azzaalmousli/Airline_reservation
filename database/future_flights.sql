-- future_flights.sql
-- Phase 2 additions: flights with 2026 departure dates.
-- Run this on top of the existing database to enable live demo bookings
-- (the trg_reservation_date_check trigger blocks booking past-dated flights).

INSERT INTO flight (flight_number, departure_iata, arrival_iata, departure_time, arrival_time, aircraft_id, status)
VALUES
  ('TK2601', 'IST', 'LHR', '2026-06-01 08:00:00', '2026-06-01 11:30:00', 'TC-JA01', 'Scheduled'),
  ('TK2602', 'LHR', 'IST', '2026-06-05 14:00:00', '2026-06-05 20:00:00', 'TC-JA01', 'Scheduled'),
  ('TK2603', 'IST', 'CDG', '2026-06-10 09:30:00', '2026-06-10 12:00:00', 'TC-JA02', 'Scheduled'),
  ('TK2604', 'CDG', 'IST', '2026-06-12 16:00:00', '2026-06-12 18:30:00', 'TC-JA02', 'Scheduled'),
  ('TK2605', 'IST', 'DXB', '2026-06-15 23:00:00', '2026-06-16 04:30:00', 'TC-JA03', 'Scheduled'),
  ('TK2606', 'DXB', 'IST', '2026-06-20 06:00:00', '2026-06-20 11:30:00', 'TC-JA03', 'Scheduled'),
  ('TK2607', 'IST', 'JFK', '2026-07-01 07:00:00', '2026-07-01 14:00:00', 'TC-JA04', 'Scheduled'),
  ('TK2608', 'JFK', 'IST', '2026-07-10 18:00:00', '2026-07-11 10:00:00', 'TC-JA04', 'Scheduled'),
  ('TK2609', 'IST', 'FRA', '2026-07-15 12:00:00', '2026-07-15 14:30:00', 'TC-JA05', 'Scheduled'),
  ('TK2610', 'FRA', 'IST', '2026-07-20 16:00:00', '2026-07-20 19:30:00', 'TC-JA05', 'Scheduled'),
  ('TK2611', 'IST', 'DOH', '2026-08-01 21:00:00', '2026-08-02 00:30:00', 'TC-JA05', 'Scheduled'),
  ('TK2612', 'DOH', 'IST', '2026-08-10 05:00:00', '2026-08-10 09:00:00', 'TC-JA05', 'Scheduled');

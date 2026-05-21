insert into airport (iata_code, name, city) values
('IST', 'istanbul airport', 'istanbul'),
('SAW', 'sabiha gokcen airport', 'istanbul'),
('LHR', 'heathrow airport', 'london'),
('CDG', 'charles de gaulle airport', 'paris'),
('DXB', 'dubai international airport', 'dubai'),
('JFK', 'john f. kennedy international airport', 'new york'),
('FRA', 'frankfurt airport', 'frankfurt'),
('DOH', 'hamad international airport', 'doha');

insert into aircraft (aircraft_id, model, seating_capacity, range_km) values
('TC-JA01', 'airbus a320', 180, 6100),
('TC-JA02', 'boeing 737-800', 189, 5700),
('TC-JA03', 'boeing 777-300', 396, 13649),
('TC-JA04', 'airbus a330', 277, 12000),
('TC-JA05', 'airbus a321', 220, 5900);

insert into customer (name, email, passport_number, date_of_birth, phone_number) values
('ahmed ali', 'ahmed.ali@example.com', 'P12345678', '1990-01-15', '+905321111111'),
('maria yildiz', 'maria.yildiz@example.com', 'P22345678', '1995-03-22', '+905322222222'),
('john smith', 'john.smith@example.com', 'P32345678', '1988-07-09', '+905323333333'),
('fatma demir', 'fatma.demir@example.com', 'P42345678', '1992-11-30', '+905324444444'),
('ali can', 'ali.can@example.com', 'P52345678', '1985-05-05', '+905325555555'),
('sara khan', 'sara.khan@example.com', 'P62345678', '1998-09-18', '+905326666666'),
('david lee', 'david.lee@example.com', 'P72345678', '1991-02-27', '+905327777777'),
('ayse kaya', 'ayse.kaya@example.com', 'P82345678', '1999-12-12', '+905328888888'),
('omar hassan', 'omar.hassan@example.com', 'P92345678', '1987-04-01', '+905329999999'),
('emma brown', 'emma.brown@example.com', 'P10345678', '1993-06-14', '+905330000000'),
('leen safi','leeno@gmail.com','P76569034','2000-06-24','+9055478965432');

insert into flight (flight_number, departure_iata, arrival_iata, departure_time, arrival_time, aircraft_id, status) values
('TK1001', 'IST', 'LHR', '2025-01-10 08:00:00', '2025-01-10 10:00:00', 'TC-JA01', 'Scheduled'),
('TK1002', 'LHR', 'IST', '2025-01-15 14:00:00', '2025-01-15 20:00:00', 'TC-JA01', 'Scheduled'),
('TK2001', 'IST', 'CDG', '2025-01-20 09:30:00', '2025-01-20 11:30:00', 'TC-JA02', 'Delayed'),
('TK2002', 'CDG', 'IST', '2025-01-22 16:00:00', '2025-01-22 18:00:00', 'TC-JA02', 'Scheduled'),
('TK3001', 'IST', 'DXB', '2025-02-01 23:00:00', '2025-02-02 04:30:00', 'TC-JA03', 'Scheduled'),
('TK3002', 'DXB', 'IST', '2025-02-05 06:00:00', '2025-02-05 11:30:00', 'TC-JA03', 'Arrived'),
('TK4001', 'IST', 'JFK', '2025-02-10 07:00:00', '2025-02-10 13:00:00', 'TC-JA04', 'Departed'),
('TK5001', 'JFK', 'IST', '2025-02-18 18:00:00', '2025-02-19 10:00:00', 'TC-JA04', 'Scheduled'),
('TK6001', 'IST', 'FRA', '2025-03-01 12:00:00', '2025-03-01 14:30:00', 'TC-JA05', 'Scheduled'),
('TK7001', 'IST', 'DOH', '2025-03-05 21:00:00', '2025-03-06 00:30:00', 'TC-JA05', 'Canceled');

insert into reservation (booking_id, customer_id, flight_number, booking_date, status) values
(1, 1, 'TK1001', '2025-01-01', 'Confirmed'),
(2, 2, 'TK1001', '2025-01-02', 'Confirmed'),
(3, 3, 'TK1002', '2025-01-05', 'Confirmed'),
(4, 4, 'TK3001', '2025-01-20', 'Confirmed'),
(5, 5, 'TK4001', '2025-01-25', 'Confirmed'),
(6, 6, 'TK6001', '2025-02-15', 'Pending'),
(7, 7, 'TK7001', '2025-02-20', 'Canceled'),
(8, 8, 'TK3002', '2025-01-28', 'Confirmed'),
(9, 9, 'TK5001', '2025-02-01', 'Confirmed'),
(10, 10, 'TK2001', '2025-01-10', 'Confirmed'),
(11, 1, 'TK2002', '2025-01-12', 'Confirmed'),
(12, 2, 'TK6001', '2025-02-18', 'Confirmed');

insert into ticket (ticket_number, seat_number, fare_class, price, payment_status, issue_date) values
(1001, '12A', 'Economy', 250.00, 'Paid', '2024-12-30 10:00:00'),
(1002, '12B', 'Economy', 250.00, 'Paid', '2024-12-30 10:05:00'),
(1003, '14A', 'Economy', 260.00, 'Paid', '2025-01-02 09:00:00'),
(1004, '14B', 'Business', 520.00, 'Paid', '2025-01-05 11:00:00'),
(1005, '15C', 'Economy', 400.00, 'Paid', '2025-01-20 08:30:00'),
(1006, '10A', 'Business', 900.00, 'Partial', '2025-01-25 13:15:00'),
(1007, '10B', 'Business', 900.00, 'Unpaid', '2025-01-25 13:20:00'),
(1008, '22C', 'Economy', 180.00, 'Paid', '2025-02-15 15:45:00'),
(1009, '1A', 'First-class', 1500.00, 'Paid', '2025-02-20 16:00:00'),
(1010, '1B', 'First-class', 1500.00, 'Paid', '2025-01-28 14:10:00'),
(1011, '2A', 'Economy', 700.00, 'Paid', '2025-02-01 09:20:00'),
(1012, '2B', 'Economy', 700.00, 'Partial', '2025-02-01 09:25:00'),
(1013, '25D', 'Economy', 280.00, 'Paid', '2025-01-10 12:00:00'),
(1014, '18F', 'Economy', 290.00, 'Paid', '2025-01-12 12:30:00'),
(1015, '7C', 'Business', 350.00, 'Unpaid', '2025-02-18 18:30:00');

insert into ticket_reservation (booking_id, ticket_number, passenger_type) values
(1, 1001, 'Adult'),
(1, 1002, 'Child'),
(2, 1003, 'Adult'),
(3, 1004, 'Adult'),
(4, 1005, 'Adult'),
(5, 1006, 'Adult'),
(5, 1007, 'Adult'),
(6, 1008, 'Child'),
(7, 1009, 'Adult'),
(8, 1010, 'Adult'),
(9, 1011, 'Adult'),
(9, 1012, 'Infant'),
(10, 1013, 'Adult'),
(11, 1014, 'Adult'),
(12, 1015, 'Adult');

insert into payment (booking_id, ticket_number, payment_date, amount, payment_method) values
( 1, 1001, '2024-12-30 10:10:00', 250.00, 'credit card'),
( 1, 1002, '2024-12-30 10:12:00', 250.00, 'credit card'),
(2, 1003, '2025-01-02 09:10:00', 260.00, 'debit card'),
( 3, 1004, '2025-01-05 11:10:00', 520.00, 'credit card'),
(4, 1005, '2025-01-20 08:40:00', 400.00, 'cash'),
( 5, 1006, '2025-01-25 13:30:00', 600.00, 'credit card'),
(6, 1008, '2025-02-15 15:50:00', 180.00, 'credit card'),
( 7, 1009, '2025-02-20 16:10:00', 1500.00, 'credit card'),
(8, 1010, '2025-01-28 14:20:00', 1500.00, 'debit card'),
( 9, 1011, '2025-02-01 09:30:00', 700.00, 'credit card'),
(10, 1013, '2025-01-10 12:10:00', 280.00, 'cash'),
(11, 1014, '2025-01-12 12:40:00', 290.00, 'credit card');

insert into address (customer_id, street, city, postal_code, country, address_type) values
(1, 'istiklal caddesi 10', 'istanbul', '34000', 'turkey', 'home'),
(2, 'bagdat caddesi 25', 'istanbul', '34728', 'turkey', 'home'),
( 3, 'oxford street 5', 'london', 'W1D 2LT', 'united kingdom', 'home'),
(4, 'rue de rivoli 12', 'paris', '75001', 'france', 'home'),
(5, 'main street 100', 'new york', '10001', 'usa', 'home'),
( 6, 'al wasl road 50', 'dubai', '00000', 'uae', 'home'),
( 7, 'zeil 20', 'frankfurt', '60313', 'germany', 'home'),
( 8, 'istiklal caddesi 22', 'istanbul', '34010', 'turkey', 'work'),
(9, 'abdullah bin jassim st', 'doha', '12345', 'qatar', 'home'),
(10, 'taksim square 3', 'istanbul', '34435', 'turkey', 'home'),
(11,'dikmen street','ankara','06540','turkey','university');

insert into system_performance_log 
(operation_name, execution_time_ms, status) values
('Insert Customer Record', 12.50, 'Success'),
('Create Flight Schedule', 18.20, 'Success'),
('Check Seat Availability', 5.10, 'Success'),
('Create Full Booking', 145.80, 'Success'),
('Process Payment', 310.45, 'Success'),
('Create Full Booking', 805.00, 'Failed - Timeout'),
('Insert Customer Record', 14.10, 'Success'),
('Check Seat Availability', 6.20, 'Success'),
('Process Payment', 285.30, 'Success'),
('Update Flight Status', 11.00, 'Success');
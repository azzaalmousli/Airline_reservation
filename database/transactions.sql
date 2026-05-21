start transaction;

-- Create reservation
insert into reservation(customer_id, flight_number, booking_date, status)
values (2, 'TK6001','2024-01-01', 'Confirmed');

set @new_booking_id = LAST_INSERT_ID();

-- Create ticket
insert into ticket(ticket_number, seat_number, fare_class, price, payment_status, issue_date)
values (2001, '30A', 'E', 300.00, 'Unpaid', NOW());

-- Link ticket to booking + passenger type
insert into ticket_reservation(booking_id, ticket_number, passenger_type)
values (@new_booking_id, 2001, 'Adult');

-- Add payment
insert into payment(booking_id, ticket_number, payment_date, amount, payment_method)
values (@new_booking_id, 2001, NOW(), 300.00, 'credit card');

commit;

start transaction;

set @cancel_booking_id = 6;

-- mark reservation canceled
update reservation
set status = 'canceled'
where booking_id = @cancel_booking_id;

-- save the unpaid ticket numbers of this booking (safe + clear)
create temporary table tmp_unpaid_tickets (
  ticket_number int primary key
);

insert into tmp_unpaid_tickets (ticket_number)
select tr.ticket_number
from ticket_reservation tr
join ticket t on t.ticket_number = tr.ticket_number
where tr.booking_id = @cancel_booking_id
  and t.payment_status = 'unpaid';

-- delete the links for those unpaid tickets
delete from ticket_reservation
where booking_id = @cancel_booking_id
  and ticket_number in (select ticket_number from tmp_unpaid_tickets);

-- delete the unpaid tickets themselves (key-based delete)
delete from ticket
where ticket_number in (select ticket_number from tmp_unpaid_tickets);

drop temporary table tmp_unpaid_tickets;

commit;

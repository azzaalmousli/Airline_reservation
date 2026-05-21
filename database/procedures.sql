delimiter $$
create procedure sp_customer_itinerary(in p_customer_id int)
begin
  select
    c.customer_id,
    c.name as customer_name,
    r.booking_id,
    r.status as reservation_status,
    f.flight_number,
    dep.name as departure_airport,
    arr.name as arrival_airport,
    f.departure_time,
    f.arrival_time,
    t.ticket_number,
    t.seat_number,
    t.fare_class,
    tr.passenger_type,
    t.price,
    t.payment_status
  from customer c
  join reservation r on r.customer_id = c.customer_id
  join flight f on f.flight_number = r.flight_number
  join airport dep on dep.iata_code = f.departure_iata
  join airport arr on arr.iata_code = f.arrival_iata
  left join ticket_reservation tr on tr.booking_id = r.booking_id
  left join ticket t on t.ticket_number = tr.ticket_number
  where c.customer_id = p_customer_id
  order by f.departure_time, r.booking_id, t.ticket_number;
end $$
delimiter ;

delimiter $$
create procedure sp_flight_sales_report(in p_flight_number char(10))
begin
  select
    f.flight_number,
    count(distinct r.booking_id) as total_bookings,
    count(distinct tr.ticket_number) as tickets_issued,
    avg(t.price) as avg_ticket_price,
    sum(p.amount) as total_paid_amount
  from flight f
  left join reservation r on r.flight_number = f.flight_number
  left join ticket_reservation tr on tr.booking_id = r.booking_id
  left join ticket t on t.ticket_number = tr.ticket_number
  left join payment p on p.ticket_number = t.ticket_number
  where f.flight_number = p_flight_number
  group by f.flight_number
  having count(distinct tr.ticket_number) >= 1;
end $$
delimiter ;

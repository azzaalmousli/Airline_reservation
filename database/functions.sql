delimiter $$
create function fn_load_factor(p_flight_number char(10))
returns decimal(6,2)
deterministic
begin
  declare v_tickets int;
  declare v_capacity int;
  select count(*)
  into v_tickets
  from reservation r
  join ticket_reservation tr on tr.booking_id = r.booking_id
  where r.flight_number = p_flight_number;

  select a.seating_capacity
  into v_capacity
  from flight f
  join aircraft a on a.aircraft_id = f.aircraft_id
  where f.flight_number = p_flight_number;

  if v_capacity is null or v_capacity = 0 then
    return 0;
  end if;
  return (v_tickets / v_capacity) * 100;
end $$
delimiter ;

delimiter $$
create function fn_total_paid_for_booking(p_booking_id int)
returns decimal(10,2)
deterministic
begin
  declare v_total decimal(10,2);

  select ifnull(sum(amount), 0)
  into v_total
  from payment
  where booking_id = p_booking_id;
  return v_total;
end $$
delimiter ;

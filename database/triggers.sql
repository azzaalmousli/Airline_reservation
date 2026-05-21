delimiter $$
create trigger trg_reservation_date_check
before insert on reservation
for each row
begin
  declare v_departure datetime;

  select departure_time
  into v_departure
  from flight
  where flight_number = new.flight_number;

  if new.booking_date > date(v_departure) then
    signal sqlstate '45000'
      set message_text = 'booking date cannot be later than flight departure date.';
  end if;
end $$
delimiter ;

delimiter $$

create trigger trg_update_ticket_payment_status
after insert on payment
for each row
begin
  declare v_total_paid decimal(10,2);
  declare v_price decimal(10,2);

  select ifnull(sum(amount), 0)
  into v_total_paid
  from payment
  where ticket_number = new.ticket_number;

  select price
  into v_price
  from ticket
  where ticket_number = new.ticket_number;

  if v_total_paid >= v_price then
    update ticket set payment_status = 'paid'
    where ticket_number = new.ticket_number;
  elseif v_total_paid > 0 then
    update ticket set payment_status = 'partial'
    where ticket_number = new.ticket_number;
  else
    update ticket set payment_status = 'unpaid'
    where ticket_number = new.ticket_number;
  end if;
end $$

delimiter ;

create view vw_customer_booking_summary as
select
  c.customer_id,
  c.name as customer_name,
  r.booking_id,
  r.status as reservation_status,
  f.flight_number,
  f.departure_time,
  f.arrival_time,
  dep.city as from_city,
  arr.city as to_city
from customer c
join reservation r on r.customer_id = c.customer_id
join flight f on f.flight_number = r.flight_number
join airport dep on dep.iata_code = f.departure_iata
join airport arr on arr.iata_code = f.arrival_iata;

create view vw_flight_financial_summary as
select
  f.flight_number,
  count(distinct tr.ticket_number) as tickets_issued,
  avg(t.price) as avg_ticket_price,
  ifnull(sum(p.amount), 0) as total_paid
from flight f
left join reservation r on r.flight_number = f.flight_number
left join ticket_reservation tr on tr.booking_id = r.booking_id
left join ticket t on t.ticket_number = tr.ticket_number
left join payment p on p.ticket_number = t.ticket_number
group by f.flight_number;

create view vw_system_stability_metrics as
select 
    operation_name,
    count(log_id) as total_runs,
    sum(case when status like '%Failed%' then 1 else 0 end) as error_count,
    round((sum(case when status like '%Failed%' then 1 else 0 end) / count(log_id)) * 100, 2) as error_rate_percent,
    avg(execution_time_ms) as avg_speed_ms,
    case 
        when avg(execution_time_ms) > 500 then 'Warning: Slow'
        when sum(case when status like '%Failed%' then 1 else 0 end) > 0 then 'Warning: Unstable'
        else 'Healthy'
    end as system_status
from system_performance_log
group by operation_name;

create view vw_cloud_infrastructure_costs as
select 
    date(recorded_at) as active_date,
    count(log_id) as total_system_transactions,
    sum(execution_time_ms) as total_compute_ms,
    -- Simulating a cloud provider (like AWS or Azure) billing $0.000005 per ms of database compute
    round(sum(execution_time_ms) * 0.000005, 4) as estimated_cloud_cost_usd
from system_performance_log
group by date(recorded_at);

select * from vw_system_stability_metrics;
select * from vw_cloud_infrastructure_costs;
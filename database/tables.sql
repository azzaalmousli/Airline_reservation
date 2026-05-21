create database airline_reservation;

create table airport (
    iata_code char(3) primary key,
    name varchar(100) not null,
    city varchar(50) not null
);
create table aircraft (
    aircraft_id varchar(10) primary key,
    model varchar(50) not null,
    seating_capacity int not null,
    range_km int,

    check (seating_capacity > 0)
);
create table customer (
    customer_id int primary key auto_increment,
    name varchar(100) not null,
    email varchar(100) unique not null,
    passport_number varchar(20) unique not null,
    date_of_birth date not null,
    phone_number varchar(20) unique);
create table flight (
    flight_number char(10) primary key,
    departure_iata char(3) not null,
    arrival_iata char(3) not null,
    departure_time datetime not null,
    arrival_time datetime not null,
    aircraft_id varchar(10),
    status varchar(20) not null,
    
    check (arrival_time > departure_time),
    check (departure_iata <> arrival_iata),
    check (status in ('Scheduled', 'Delayed', 'Arrived', 'Departed', 'Canceled')),
    
    foreign key (departure_iata) references airport(iata_code),
    foreign key (arrival_iata) references airport(iata_code),
    foreign key (aircraft_id) references aircraft(aircraft_id)
);
create table reservation (
    booking_id int primary key auto_increment,
    customer_id int not null,
    flight_number char(10) not null,
    booking_date date not null,
    status varchar(20) not null,
    
    foreign key (customer_id) references customer(customer_id),
    foreign key (flight_number) references flight(flight_number)
);
create table ticket (
    ticket_number int primary key,
    seat_number varchar(5) not null unique,
   fare_class varchar(15),
    price decimal(10, 2) not null,
    payment_status varchar(20) not null,
    issue_date datetime not null
);
create table ticket_reservation (
    booking_id int not null,
    ticket_number int not null,
	   passenger_type varchar(10) not null default 'Adult',
    constraint chk_passenger_type
	   check (passenger_type in ('Adult', 'Child', 'Infant')),
    
    primary key (booking_id, ticket_number),
    foreign key (booking_id) references reservation(booking_id),
    foreign key (ticket_number) references ticket(ticket_number)
);


create table payment (
    payment_id int primary key auto_increment,
    booking_id int not null,
    ticket_number int not null,
    payment_date datetime not null,
    amount decimal(10, 2) not null,
    payment_method varchar(50) not null,
    check (amount > 0),
    
    foreign key (ticket_number) references ticket(ticket_number)
);
create table address (
    address_id int primary key auto_increment,
    customer_id int not null,
    street varchar(100),
    city varchar(50) not null,
    postal_code varchar(10),
    country varchar(50) not null,
    address_type varchar(20) not null,
    
    foreign key (customer_id) references customer(customer_id)
);
create table system_performance_log (
    log_id int primary key auto_increment,
    operation_name varchar(100) not null,
    execution_time_ms decimal(10,2) not null,
    recorded_at datetime(3) default current_timestamp(3),
    status varchar(20) default 'Success'
);


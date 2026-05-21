# models.py
from sqlalchemy import Column, String, Integer, DateTime, Date, Decimal, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Airport(Base):
    __tablename__ = 'airport'
    
    iata_code = Column(String(3), primary_key=True)
    name = Column(String(100), nullable=False)
    city = Column(String(50), nullable=False)
    
    # Relationships
    departing_flights = relationship("Flight", foreign_keys="[Flight.departure_iata]", back_populates="departure_airport")
    arriving_flights = relationship("Flight", foreign_keys="[Flight.arrival_iata]", back_populates="arrival_airport")


class Aircraft(Base):
    __tablename__ = 'aircraft'
    
    aircraft_id = Column(String(10), primary_key=True)
    model = Column(String(50), nullable=False)
    seating_capacity = Column(Integer, nullable=False)
    range_km = Column(Integer)
    
    __table_args__ = (CheckConstraint('seating_capacity > 0'),)
    
    flights = relationship("Flight", back_populates="aircraft")


class Customer(Base):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    passport_number = Column(String(20), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    phone_number = Column(String(20), unique=True)
    
    reservations = relationship("Reservation", back_populates="customer")
    addresses = relationship("Address", back_populates="customer")


class Flight(Base):
    __tablename__ = 'flight'
    
    flight_number = Column(String(10), primary_key=True)
    departure_iata = Column(String(3), ForeignKey('airport.iata_code'), nullable=False)
    arrival_iata = Column(String(3), ForeignKey('airport.iata_code'), nullable=False)
    departure_time = Column(DateTime, nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    aircraft_id = Column(String(10), ForeignKey('aircraft.aircraft_id'))
    status = Column(String(20), nullable=False)
    
    __table_args__ = (
        CheckConstraint('arrival_time > departure_time'),
        CheckConstraint('departure_iata <> arrival_iata'),
        CheckConstraint("status IN ('Scheduled', 'Delayed', 'Arrived', 'Departed', 'Canceled')"),
    )
    
    # Explicit mapping for dual-airport foreign keys
    departure_airport = relationship("Airport", foreign_keys=[departure_iata], back_populates="departing_flights")
    arrival_airport = relationship("Airport", foreign_keys=[arrival_iata], back_populates="arriving_flights")
    aircraft = relationship("Aircraft", back_populates="flights")
    reservations = relationship("Reservation", back_populates="flight")


class Reservation(Base):
    __tablename__ = 'reservation'
    
    booking_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    flight_number = Column(String(10), ForeignKey('flight.flight_number'), nullable=False)
    booking_date = Column(Date, nullable=False)
    status = Column(String(20), nullable=False)
    
    customer = relationship("Customer", back_populates="reservations")
    flight = relationship("Flight", back_populates="reservations")
    tickets = relationship("TicketReservation", back_populates="reservation")


class Ticket(Base):
    __tablename__ = 'ticket'
    
    ticket_number = Column(Integer, primary_key=True)
    seat_number = Column(String(5), unique=True, nullable=False)
    fare_class = Column(String(15))
    price = Column(Decimal(10, 2), nullable=False)
    payment_status = Column(String(20), nullable=False)
    issue_date = Column(DateTime, nullable=False)
    
    reservations = relationship("TicketReservation", back_populates="ticket")
    payments = relationship("Payment", back_populates="ticket")


class TicketReservation(Base):
    __tablename__ = 'ticket_reservation'
    
    booking_id = Column(Integer, ForeignKey('reservation.booking_id'), primary_key=True)
    ticket_number = Column(Integer, ForeignKey('ticket.ticket_number'), primary_key=True)
    passenger_type = Column(String(10), nullable=False, default='Adult')
    
    __table_args__ = (CheckConstraint("passenger_type IN ('Adult', 'Child', 'Infant')"),)
    
    reservation = relationship("Reservation", back_populates="tickets")
    ticket = relationship("Ticket", back_populates="reservations")


class Payment(Base):
    __tablename__ = 'payment'
    
    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    booking_id = Column(Integer, nullable=False)
    ticket_number = Column(Integer, ForeignKey('ticket.ticket_number'), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Decimal(10, 2), nullable=False)
    payment_method = Column(String(50), nullable=False)
    
    __table_args__ = (CheckConstraint('amount > 0'),)
    
    ticket = relationship("Ticket", back_populates="payments")


class Address(Base):
    __tablename__ = 'address'
    
    address_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'), nullable=False)
    street = Column(String(100))
    city = Column(String(50), nullable=False)
    postal_code = Column(String(10))
    country = Column(String(50), nullable=False)
    address_type = Column(String(20), nullable=False)
    
    customer = relationship("Customer", back_populates="addresses")


class SystemPerformanceLog(Base):
    __tablename__ = 'system_performance_log'
    
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    operation_name = Column(String(100), nullable=False)
    execution_time_ms = Column(Decimal(10, 2), nullable=False)
    recorded_at = Column(DateTime, default=None)  # Handled natively or dynamically
    status = Column(String(20), default='Success')
# schemas.py
from pydantic import BaseModel, EmailStr, Field, model_validator
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

# ==========================================
# AIRPORT SCHEMAS
# ==========================================
class AirportBase(BaseModel):
    iata_code: str = Field(..., min_length=3, max_length=3, description="3-letter airport code")
    name: str = Field(..., max_length=100)
    city: str = Field(..., max_length=50)

class AirportCreate(AirportBase):
    pass

class AirportResponse(AirportBase):
    class Config:
        from_attributes = True

# ==========================================
# CUSTOMER SCHEMAS
# ==========================================
class CustomerBase(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    passport_number: str = Field(..., max_length=20)
    date_of_birth: date
    phone_number: Optional[str] = Field(None, max_length=20)

class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    customer_id: int
    class Config:
        from_attributes = True

# ==========================================
# FLIGHT SCHEMAS
# ==========================================
class FlightBase(BaseModel):
    flight_number: str = Field(..., max_length=10)
    departure_iata: str = Field(..., min_length=3, max_length=3)
    arrival_iata: str = Field(..., min_length=3, max_length=3)
    departure_time: datetime
    arrival_time: datetime
    aircraft_id: Optional[str] = Field(None, max_length=10)
    status: str = Field('Scheduled', description="Scheduled, Delayed, Arrived, Departed, Canceled")

class FlightCreate(FlightBase):
    @model_validator(mode='after')
    def validate_flight_logic(self):
        if self.arrival_time <= self.departure_time:
            raise ValueError("arrival_time must occur explicitly after departure_time")
        if self.departure_iata == self.arrival_iata:
            raise ValueError("Departure airport and Arrival airport cannot match")
        if self.status not in ['Scheduled', 'Delayed', 'Arrived', 'Departed', 'Canceled']:
            raise ValueError("Invalid flight state classification status")
        return self

class FlightResponse(FlightBase):
    class Config:
        from_attributes = True

# ==========================================
# RESERVATION SCHEMAS
# ==========================================
class ReservationBase(BaseModel):
    customer_id: int
    flight_number: str = Field(..., max_length=10)
    booking_date: date
    status: str = Field(..., max_length=20)

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(ReservationBase):
    booking_id: int
    class Config:
        from_attributes = True

# ==========================================
# TICKET & PAYMENT SCHEMAS
# ==========================================
class TicketBase(BaseModel):
    ticket_number: int
    seat_number: str = Field(..., max_length=5)
    fare_class: Optional[str] = Field(None, max_length=15)
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    payment_status: str = Field(..., max_length=20)
    issue_date: datetime

class TicketCreate(TicketBase):
    pass

class PaymentCreate(BaseModel):
    booking_id: int
    ticket_number: int
    payment_date: datetime
    amount: Decimal = Field(..., gt=0, max_digits=10, decimal_places=2)
    payment_method: str = Field(..., max_length=50)
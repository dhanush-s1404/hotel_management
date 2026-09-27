from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=128)
    role: str = "staff"


class UserLogin(BaseModel):
    email: str = Field(..., max_length=255)
    password: str = Field(..., min_length=6, max_length=128)


class User(BaseModel):
    id: str
    name: str
    email: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


# Room schemas
class RoomCreate(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=20)
    room_type: str = Field(..., min_length=1, max_length=50)
    floor: int = Field(..., ge=1)
    capacity: int = Field(..., ge=1)
    price_per_night: float = Field(..., gt=0)
    description: Optional[str] = None
    status: str = "available"


class RoomUpdate(BaseModel):
    room_number: Optional[str] = Field(None, min_length=1, max_length=20)
    room_type: Optional[str] = Field(None, min_length=1, max_length=50)
    floor: Optional[int] = Field(None, ge=1)
    capacity: Optional[int] = Field(None, ge=1)
    price_per_night: Optional[float] = Field(None, gt=0)
    description: Optional[str] = None
    status: Optional[str] = None


class Room(BaseModel):
    id: str
    room_number: str
    room_type: str
    floor: int
    capacity: int
    price_per_night: float
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Customer schemas
class CustomerCreate(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=200)
    phone: str = Field(..., min_length=1, max_length=20)
    email: str = Field(..., max_length=255)
    address: Optional[str] = None
    id_proof_type: str = Field(..., min_length=1, max_length=50)
    id_proof_number: str = Field(..., min_length=1, max_length=50)


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=200)
    phone: Optional[str] = Field(None, min_length=1, max_length=20)
    email: Optional[str] = Field(None, max_length=255)
    address: Optional[str] = None
    id_proof_type: Optional[str] = Field(None, min_length=1, max_length=50)
    id_proof_number: Optional[str] = Field(None, min_length=1, max_length=50)


class Customer(BaseModel):
    id: str
    full_name: str
    phone: str
    email: str
    address: Optional[str]
    id_proof_type: str
    id_proof_number: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Booking schemas
class BookingCreate(BaseModel):
    customer_id: str
    room_id: str
    check_in_date: str
    check_out_date: str
    guests: int = 1


class BookingUpdate(BaseModel):
    status: Optional[str] = None
    guests: Optional[int] = Field(None, ge=1)


class Booking(BaseModel):
    id: str
    booking_reference: str
    customer: Optional[User] = None
    room: Optional[Room] = None
    check_in_date: str
    check_out_date: str
    actual_check_in: Optional[str] = None
    actual_check_out: Optional[str] = None
    guests: int
    status: str
    total_amount: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Payment schemas
class PaymentCreate(BaseModel):
    booking_id: str
    amount: float = Field(..., gt=0)
    payment_method: str = Field(..., min_length=1, max_length=50)
    payment_status: str = "pending"


class PaymentUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    payment_method: Optional[str] = Field(None, min_length=1, max_length=50)
    payment_status: Optional[str] = None


class Payment(BaseModel):
    id: str
    booking_id: str
    amount: float
    payment_method: str
    payment_status: str
    payment_date: datetime
    transaction_reference: Optional[str] = None

    class Config:
        from_attributes = True


# Search schemas
class RoomSearch(BaseModel):
    room_type: Optional[str] = None
    status: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_capacity: Optional[int] = None


class CustomerSearch(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class BookingSearch(BaseModel):
    customer_id: Optional[str] = None
    room_id: Optional[str] = None
    status: Optional[str] = None
    check_in_date: Optional[str] = None
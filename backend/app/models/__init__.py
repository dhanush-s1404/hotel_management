"""SQLAlchemy models for Hotel Management System."""

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Date,
    Boolean,
    Text,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="staff", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("Bookings", back_populates="customer")


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    room_number = Column(String, unique=True, nullable=False)
    room_type = Column(String, nullable=False)
    floor = Column(Integer, nullable=False)
    capacity = Column(Integer, nullable=False)
    price_per_night = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String, default="available", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("Bookings", back_populates="room")


class Customers(Base):
    __tablename__ = "customers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(Text, nullable=True)
    id_proof_type = Column(String, nullable=False)
    id_proof_number = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bookings = relationship("Bookings", back_populates="customer")


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_reference = Column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4())[:8].upper())
    customer_id = Column(String, ForeignKey("users.id"), nullable=False)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False)
    check_in_date = Column(Date, nullable=False)
    check_out_date = Column(Date, nullable=False)
    actual_check_in = Column(DateTime, nullable=True)
    actual_check_out = Column(DateTime, nullable=True)
    guests = Column(Integer, nullable=False, default=1)
    status = Column(String, default="pending", nullable=False)
    total_amount = Column(Float, nullable=True, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = relationship("Users", back_populates="bookings")
    room = relationship("Rooms", back_populates="bookings")
    payments = relationship("Payments", back_populates="booking", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("room_id", "check_in_date", "check_out_date", name="unique_room_date_booking"),
    )


class Payments(Base):
    __tablename__ = "payments"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_id = Column(String, ForeignKey("bookings.id"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    payment_status = Column(String, default="pending", nullable=False)
    payment_date = Column(DateTime, default=datetime.utcnow)
    transaction_reference = Column(String, nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    booking = relationship("Bookings", back_populates="payments")
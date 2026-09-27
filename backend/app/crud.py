"""CRUD operations for Hotel Management System."""

from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_


# Lazy imports to avoid circular dependencies
def _import_models():
    from app.models import Users, Rooms, Customers, Bookings, Payments
    return Users, Rooms, Customers, Bookings, Payments


USERS, ROOMS, CUSTOMERS, BOOKINGS, PAYMENTS = _import_models()


# Users CRUD
def get_user(db: Session, user_id: str) -> USERS:
    return db.query(USERS).filter(USERS.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> USERS:
    return db.query(USERS).filter(USERS.email == email).first()


def create_user(db: Session, user: USERS) -> USERS:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Rooms CRUD
def get_room(db: Session, room_id: str) -> ROOMS:
    return db.query(ROOMS).filter(ROOMS.id == room_id).first()


def get_room_by_number(db: Session, room_number: str) -> ROOMS:
    return db.query(ROOMS).filter(ROOMS.room_number == room_number).first()


def get_rooms(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    room_type: Optional[str] = None,
) -> list[ROOMS]:
    query = db.query(ROOMS)
    if status:
        query = query.filter(ROOMS.status == status)
    if room_type:
        query = query.filter(ROOMS.room_type == room_type)
    return query.offset(skip).limit(limit).all()


def create_room(db: Session, room: ROOMS) -> ROOMS:
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


def update_room(db: Session, room_id: str, room_data: dict) -> ROOMS:
    db.query(ROOMS).filter(ROOMS.id == room_id).update(room_data)
    db.commit()
    return get_room(db, room_id)


def delete_room(db: Session, room_id: str) -> bool:
    db.query(ROOMS).filter(ROOMS.id == room_id).delete()
    db.commit()
    return True


# Customers CRUD
def get_customer(db: Session, customer_id: str) -> CUSTOMERS:
    return db.query(CUSTOMERS).filter(CUSTOMERS.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> CUSTOMERS:
    return db.query(CUSTOMERS).filter(CUSTOMERS.email == email).first()


def get_customer_by_id_proof(db: Session, id_proof_number: str) -> CUSTOMERS:
    return db.query(CUSTOMERS).filter(Customers.id_proof_number == id_proof_number).first()


def get_customers(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> list[CUSTOMERS]:
    query = db.query(CUSTOMERS)
    if search:
        query = query.filter(
            or_(
                CUSTOMERS.full_name.ilike(f"%{search}%"),
                CUSTOMERS.phone.ilike(f"%{search}%"),
            )
        )
    return query.offset(skip).limit(limit).all()


def create_customer(db: Session, customer: CUSTOMERS) -> CUSTOMERS:
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def update_customer(db: Session, customer_id: str, customer_data: dict) -> CUSTOMERS:
    db.query(CUSTOMERS).filter(CUSTOMERS.id == customer_id).update(customer_data)
    db.commit()
    return get_customer(db, customer_id)


def delete_customer(db: Session, customer_id: str) -> bool:
    db.query(CUSTOMERS).filter(CUSTOMERS.id == customer_id).delete()
    db.commit()
    return True


# Bookings CRUD
def get_booking(db: Session, booking_id: str) -> BOOKINGS:
    return db.query(BOOKINGS).filter(BOOKINGS.id == booking_id).first()


def get_booking_by_reference(db: Session, reference: str) -> BOOKINGS:
    return db.query(BOOKINGS).filter(BOOKINGS.booking_reference == reference).first()


def get_bookings(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    room_id: Optional[str] = None,
) -> list[BOOKINGS]:
    query = db.query(BOOKINGS)
    if status:
        query = query.filter(BOOKINGS.status == status)
    if customer_id:
        query = query.filter(BOOKINGS.customer_id == customer_id)
    if room_id:
        query = query.filter(BOOKINGS.room_id == room_id)
    return query.offset(skip).limit(limit).all()


def create_booking(db: Session, booking: BOOKINGS) -> BOOKINGS:
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def update_booking(db: Session, booking_id: str, booking_data: dict) -> BOOKINGS:
    db.query(BOOKINGS).filter(BOOKINGS.id == booking_id).update(booking_data)
    db.commit()
    return get_booking(db, booking_id)


def cancel_booking(db: Session, booking_id: str) -> BOOKINGS:
    booking = get_booking(db, booking_id)
    if booking:
        booking.status = "cancelled"
        db.commit()
        db.refresh(booking)
    return booking


def check_room_availability(
    db: Session,
    room_id: str,
    check_in_date: date,
    check_out_date: date,
    exclude_booking_id: Optional[str] = None,
) -> bool:
    """Check if a room is available for the given date range.
    Returns True if available, False if there's an overlap."""
    query = (
        db.query(BOOKINGS)
        .filter(
            BOOKINGS.room_id == room_id,
            BOOKINGS.status != "cancelled",
            BOOKINGS.check_in_date <= check_out_date,
            BOOKINGS.check_out_date >= check_in_date,
        )
    )
    if exclude_booking_id:
        query = query.filter(BOOKINGS.id != exclude_booking_id)
    
    overlapping = query.first()
    return overlapping is None


# Payments CRUD
def get_payment(db: Session, payment_id: str) -> PAYMENTS:
    return db.query(PAYMENTS).filter(PAYMENTS.id == payment_id).first()


def get_payment_by_booking(db: Session, booking_id: str) -> PAYMENTS:
    return db.query(PAYMENTS).filter(PAYMENTS.booking_id == booking_id).first()


def get_payments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    booking_id: Optional[str] = None,
) -> list[PAYMENTS]:
    query = db.query(PAYMENTS)
    if booking_id:
        query = query.filter(PAYMENTS.booking_id == booking_id)
    return query.offset(skip).limit(limit).all()


def create_payment(db: Session, payment: PAYMENTS) -> PAYMENTS:
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment


def update_payment(db: Session, payment_id: str, payment_data: dict) -> PAYMENTS:
    db.query(PAYMENTS).filter(PAYMENTS.id == payment_id).update(payment_data)
    db.commit()
    return get_payment(db, payment_id)
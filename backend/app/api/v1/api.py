from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import date
from app.models import Users

from app.core.database import get_db
from app.crud import (
    get_user, get_user_by_email, create_user,
    get_room, get_rooms, create_room, update_room, delete_room,
    get_customer, get_customers, create_customer, update_customer, delete_customer,
    get_booking, get_bookings, create_booking, update_booking, cancel_booking,
    check_room_availability, get_payment, get_payments, create_payment, update_payment,
)
from app.auth import create_access_token, verify_password, get_current_user, require_admin, require_staff, require_authenticated_user
from app.schemas import (
    UserCreate, UserLogin, User,
    RoomCreate, RoomUpdate, Room,
    CustomerCreate, CustomerUpdate, Customer,
    BookingCreate, BookingUpdate, Booking,
    PaymentCreate, PaymentUpdate, Payment,
)

router = APIRouter(prefix="/api/v1", tags=["Hotel Management"])


# Auth endpoints
@router.post("/auth/login", response_model=dict)
async def login(
    user_login: UserLogin,
    db: Session = Depends(get_db),
):
    user = get_user_by_email(db, user_login.email)
    if not user or not verify_password(user_login.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    from datetime import timedelta
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
    }


@router.post("/auth/logout")
async def logout(
    current_user: Users = Depends(get_user_by_id),
):
    return {"message": "Successfully logged out"}


# Room endpoints
@router.get("/rooms", response_model=List[Room])
async def list_rooms(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    room_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    rooms = get_rooms(db, skip=skip, limit=limit, status=status, room_type=room_type)
    return rooms


@router.post("/rooms", response_model=Room)
async def create_room_endpoint(
    room: RoomCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_admin),
):
    db_room = get_room_by_number(db, room.room_number)
    if db_room:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room number already exists",
        )
    db_room = create_room(db, room=room)
    return db_room


@router.get("/rooms/{room_id}", response_model=Room)
async def get_room_endpoint(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    db_room = get_room(db, room_id=room_id)
    if not db_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return db_room


@router.put("/rooms/{room_id}", response_model=Room)
async def update_room_endpoint(
    room_id: str,
    room: RoomUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_admin),
):
    db_room = update_room(db, room_id, room.model_dump(exclude_unset=True))
    if not db_room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return db_room


@router.delete("/rooms/{room_id}")
async def delete_room_endpoint(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_admin),
):
    success = delete_room(db, room_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    return {"message": "Room deleted successfully"}


# Customer endpoints
@router.get("/customers", response_model=List[Customer])
async def list_customers(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    customers = get_customers(db, skip=skip, limit=limit, search=search)
    return customers


@router.post("/customers", response_model=Customer)
async def create_customer_endpoint(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    db_customer = get_customer_by_email(db, customer.email)
    if db_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer email already exists",
        )
    db_customer_by_phone = get_customer_by_id_proof(db, customer.id_proof_number)
    if db_customer_by_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer ID proof number already exists",
        )
    db_customer = create_customer(db, customer=customer)
    return db_customer


@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer_endpoint(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    db_customer = get_customer(db, customer_id=customer_id)
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    # Customers can only access their own data, staff/admin can access any
    if current_user.role != "admin" and current_user.id != db_customer.id:
        # Actually customer_id is the user ID, and current_user is the authenticated user
        # We need to check if the current user is authorized to view this customer
        # For now, staff/admin can view any customer, customers can only view their own
        if current_user.role == "customer" and current_user.id != customer_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this customer's data",
            )
    return db_customer


@router.put("/customers/{customer_id}", response_model=Customer)
async def update_customer_endpoint(
    customer_id: str,
    customer: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    db_customer = update_customer(db, customer_id, customer.model_dump(exclude_unset=True))
    if not db_customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return db_customer


@router.delete("/customers/{customer_id}")
async def delete_customer_endpoint(
    customer_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    success = delete_customer(db, customer_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return {"message": "Customer deleted successfully"}


# Booking endpoints
@router.get("/bookings", response_model=List[Booking])
async def list_bookings(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    # Customers can only see their own bookings; staff/admin can see all
    query_customer_id = current_user.id if current_user.role == "customer" else customer_id
    bookings = get_bookings(
        db, skip=skip, limit=limit, status=status, customer_id=query_customer_id, room_id=None
    )
    return bookings


@router.post("/bookings", response_model=Booking)
async def create_booking_endpoint(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    # Set the customer_id to the authenticated user
    booking_data = booking.model_dump()
    booking_data["customer_id"] = current_user.id
    
    # Validate customer exists (using the authenticated user's ID)
    customer = get_user(db, user_id=current_user.id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    
    # Validate room exists
    room = get_room(db, room_id=booking.room_id)
    if not room:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Room not found",
        )
    
    # Check room availability
    check_in = date.fromisoformat(booking.check_in_date)
    check_out = date.fromisoformat(booking.check_out_date)
    
    if check_out <= check_in:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Check-out date must be after check-in date",
        )
    
    is_available = check_room_availability(
        db, booking.room_id, check_in, check_out
    )
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Room is not available for the selected dates (overlapping booking)",
        )
    
    # Calculate number of nights and total amount
    nights = (check_out - check_in).days
    total_amount = nights * room.price_per_night
    
    # Create the booking
    db_booking = Bookings(
        customer_id=current_user.id,
        room_id=booking.room_id,
        check_in_date=check_in,
        check_out_date=check_out,
        guests=booking.guests,
        status="pending",
        total_amount=total_amount,
    )
    
    db_booking = create_booking(db, db_booking)
    
    # Update room status to reserved
    room.status = "reserved"
    db.commit()
    
    return db_booking


@router.get("/bookings/{booking_id}", response_model=Booking)
async def get_booking_endpoint(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    db_booking = get_booking(db, booking_id=booking_id)
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    # Prevent IDOR: customers can only access their own bookings
    if current_user.role == "customer" and db_booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail "Not authorized to access this booking",
        )
    return db_booking


@router.put("/bookings/{booking_id}", response_model=Booking)
async def update_booking_endpoint(
    booking_id: str,
    booking: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    db_booking = update_booking(db, booking_id, booking.model_dump(exclude_unset=True))
    if not db_booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    return db_booking


@router.post("/bookings/{booking_id}/check-in")
async def check_in_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    booking = get_booking(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    if booking.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be checked in - status is not pending",
        )
    
    # Update booking status
    booking.status = "checked-in"
    booking.actual_check_in = datetime.utcnow()
    
    # Update room status to occupied
    room = get_room(db, room_id=booking.room_id)
    if room:
        room.status = "occupied"
    
    db.commit()
    db.refresh(booking)
    
    return {"message": "Check-in successful", "booking_id": booking.id, "actual_check_in": booking.actual_check_in}


@router.post("/bookings/{booking_id}/check-out")
async def check_out_booking(
    booking_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    booking = get_booking(db, booking_id=booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    if booking.status != "checked-in":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking cannot be checked out - status is not checked-in",
        )
    
    # Update booking status
    booking.status = "checked-out"
    booking.actual_check_out = datetime.utcnow()
    
    # Calculate total nights and amount
    if booking.actual_check_in:
        nights = (booking.actual_check_out - booking.actual_check_in).days
        # Use the room's current price per night
        room = get_room(db, room_id=booking.room_id)
        if room:
            booking.total_amount = nights * room.price_per_night
    
    # Update room status to available
    if room:
        room.status = "available"
    
    db.commit()
    db.refresh(booking)
    
    return {"message": "Check-out successful", "booking_id": booking.id, "actual_check_out": booking.actual_check_out, "total_amount": booking.total_amount}


# Payment endpoints
@router.get("/payments", response_model=List[Payment])
async def list_payments(
    skip: int = 0,
    limit: int = 100,
    booking_id: Optional[str] = None,
    db: Session = Depends(get_db),
):
    payments = get_payments(db, skip=skip, limit=limit, booking_id=booking_id)
    return payments


@router.post("/payments", response_model=Payment)
async def create_payment_endpoint(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_staff),
):
    # Check if booking exists
    booking = get_booking(db, booking_id=payment.booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found",
        )
    
    # Prevent IDOR: customers can only pay for their own bookings
    if current_user.role == "customer" and booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to pay for this booking",
        )
    
    # BACKEND VALIDATION: Calculate the authoritative booking total from database data
    # Never trust the frontend payment amount
    check_in = booking.check_in_date
    check_out = booking.check_out_date
    nights = (check_out - check_in).days
    expected_total = nights * booking.room.price_per_night
    
    # Validate the payment amount matches the expected total
    if payment.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment amount must be positive",
        )
    
    if payment.amount > expected_total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Payment amount exceeds booking total of {expected_total}",
        )
    
    # Check if payment already exists for this booking
    existing_payment = get_payment_by_booking(db, booking_id=payment.booking_id)
    if existing_payment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payment already exists for this booking",
        )
    
    db_payment = Payments(
        booking_id=payment.booking_id,
        amount=payment.amount,
        payment_method=payment.payment_method,
        payment_status=payment.payment_status,
    )
    
    db_payment = create_payment(db, db_payment)
    
    # Update booking payment status based on cumulative payments
    db.commit()
    
    return db_payment


@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment_endpoint(
    payment_id: str,
    db: Session = Depends(get_db),
    current_user: Users = Depends(require_authenticated_user),
):
    db_payment = get_payment(db, payment_id=payment_id)
    if not db_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    # Prevent IDOR: customers can only access payments for their own bookings
    booking = get_booking(db, booking_id=db_payment.booking_id)
    if current_user.role == "customer" and booking.customer_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this payment",
        )
    return db_payment


@router.get("/payments/{payment_id}", response_model=Payment)
async def get_payment_endpoint(
    payment_id: str,
    db: Session = Depends(get_db),
):
    db_payment = get_payment(db, payment_id=payment_id)
    if not db_payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    return db_payment
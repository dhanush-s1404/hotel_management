"""Initial migration

Revision ID: 9943763e8fd1
Revises: 
Create Date: 2026-09-21 08:12:48.320049

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9943763e8fd1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("role", sa.String, default="staff", nullable=False),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "rooms",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("room_number", sa.String, unique=True, nullable=False),
        sa.Column("room_type", sa.String, nullable=False),
        sa.Column("floor", sa.Integer, nullable=False),
        sa.Column("capacity", sa.Integer, nullable=False),
        sa.Column("price_per_night", sa.Float, nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("status", sa.String, default="available", nullable=False),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "customers",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("full_name", sa.String, nullable=False),
        sa.Column("phone", sa.String, nullable=False),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("address", sa.Text, nullable=True),
        sa.Column("id_proof_type", sa.String, nullable=False),
        sa.Column("id_proof_number", sa.String, nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_table(
        "bookings",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("booking_reference", sa.String, unique=True, nullable=False),
        sa.Column("customer_id", sa.String, nullable=False),
        sa.Column("room_id", sa.String, nullable=False),
        sa.Column("check_in_date", sa.Date, nullable=False),
        sa.Column("check_out_date", sa.Date, nullable=False),
        sa.Column("actual_check_in", sa.DateTime, nullable=True),
        sa.Column("actual_check_out", sa.DateTime, nullable=True),
        sa.Column("guests", sa.Integer, nullable=False, default=1),
        sa.Column("status", sa.String, default="pending", nullable=False),
        sa.Column("total_amount", sa.Float, nullable=True, default=0.0),
        sa.Column("created_at", sa.DateTime, default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime, default=sa.func.now(), onupdate=sa.func.now()),
        sa.ForeignKeyConstraint(["customer_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["room_id"], ["rooms.id"]),
        sa.UniqueConstraint("room_id", "check_in_date", "check_out_date", name="unique_room_date_booking"),
    )
    op.create_table(
        "payments",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("booking_id", sa.String, nullable=False),
        sa.Column("amount", sa.Float, nullable=False),
        sa.Column("payment_method", sa.String, nullable=False),
        sa.Column("payment_status", sa.String, default="pending", nullable=False),
        sa.Column("payment_date", sa.DateTime, default=sa.func.now()),
        sa.Column("transaction_reference", sa.String, nullable=True, unique=True),
    )
    op.create_foreign_key(
        "payments_booking_id_fkey", "payments", "bookings", ["booking_id"], ["id"]
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("payments")
    op.drop_table("bookings")
    op.drop_table("customers")
    op.drop_table("rooms")
    op.drop_table("users")
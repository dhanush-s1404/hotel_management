import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.database import Base

target_metadata = Base.metadata


def run_migrations_offline():
    """Run migrations in 'offline mode'.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is obtained
    from the URL.
    """
    url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hotel_management")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online mode'.
    
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    connectable = engine_from_config(
        {"sqlalchemy.url": os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/hotel_management")},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
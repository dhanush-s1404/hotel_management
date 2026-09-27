import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Clear any cached modules related to our app
for mod in list(sys.modules.keys()):
    if 'app' in mod:
        del sys.modules[mod]

# Import in the right order
from app.core.database import Base, engine, SessionLocal
print('Imported core.database')

from app.models import Users, Rooms, Customers, Bookings, Payments
print('Imported models')

from app.schemas import *
print('Imported schemas')

from app.crud import *
print('Imported crud')

from app.auth import *
print('Imported auth')

from app.api.v1.api import *
print('Imported api.v1.api')

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

print('\nApp created successfully!')
print('Routes:', [route.path for route in app.routes])
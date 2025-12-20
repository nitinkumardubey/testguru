from fastapi import FastAPI
from database import engine
from models import Base
from routers import users

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="User CRUD API with Images")

# Include routers
app.include_router(users.router)

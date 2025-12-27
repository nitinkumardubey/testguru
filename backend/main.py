from fastapi import FastAPI
from database import engine
from models import Base
from routers import users, admin, api_management, api_logger
from routers.api_logger import ApiLoggerMiddleware

# Create tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="User CRUD API with Images")

# Register middleware
app.add_middleware(ApiLoggerMiddleware)

# Include routers
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(api_management.router)
app.include_router(api_logger.router)

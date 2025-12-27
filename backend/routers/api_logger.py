import time
import json
from fastapi import Request, APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware
from database import SessionLocal
from models import ApiLog
from schemas import APILogSchema
from database import get_db


router = APIRouter(prefix="/api_logs", tags=["API Logs"])

EXCLUDED_APIS = ["/health", "/openapi.json", "/docs"]

@router.get("/logs", response_model=List[APILogSchema])
def get_logs(
    path: Optional[str] = Query(None),
    method: Optional[str] = Query(None),
    ip_address: Optional[str] = Query(None)
):
    db = next(get_db())
    query = db.query(ApiLog)

    if path:
        query = query.filter(ApiLog.path == path)
    if method:
        query = query.filter(ApiLog.method.ilike(method))
    if ip_address:
        query = query.filter(ApiLog.ip_address == ip_address)

    query = query.order_by(ApiLog.created_at.desc())
    logs = query.all()
    return [APILogSchema.from_orm(log) for log in logs]

class ApiLoggerMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_APIS:
            return await call_next(request)

        start_time = time.time()

        # Get client IP (supports proxies)
        ip_address = request.headers.get("x-forwarded-for")
        if ip_address:
            ip_address = ip_address.split(",")[0]
        else:
            ip_address = request.client.host if request.client else None

        # Read request body safely
        request_body = None
        if request.method in ("POST", "PUT", "PATCH"):
            try:
                body_bytes = await request.body()
                request_body = json.loads(body_bytes) if body_bytes else None
            except Exception:
                request_body = None

        response = await call_next(request)

        response_time_ms = int((time.time() - start_time) * 1000)

        # Save log to DB
        db = SessionLocal()
        db.add(ApiLog(
            path=request.url.path,
            method=request.method,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            ip_address=ip_address,
            request_body=request_body
        ))
        db.commit()
        db.close()

        return response

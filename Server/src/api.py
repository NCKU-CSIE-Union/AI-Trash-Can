from typing import Annotated
from fastapi import APIRouter, Depends, Response, Form, HTTPException, status
from fastapi.responses import JSONResponse

from src.schema import Record, Filters
from src.model import Service
from src.security import required_login, create_token
from src.config import server_config

public_api_router = APIRouter()
private_api_router = APIRouter(prefix="/api", dependencies=[Depends(required_login)])

def get_filters(seen: bool = None, created_at_start: int = None, created_at_end: int = None):
    return Filters(seen=seen, created_at_start=created_at_start, created_at_end=created_at_end)

def get_service():
    return Service()

@public_api_router.get("/api/health/")
def health():
    return {"status": "ok"}

@public_api_router.post("/api/login/")
def login(response: Response, username: Annotated[str, Form()], password: Annotated[str, Form()]):
    if username != server_config.auth.USERNAME or password != server_config.auth.PASSWORD:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content={"message": "login successful"}
    )
    response.set_cookie(
        key="auth",
        value=create_token(username),
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=server_config.auth.EXPIRE_MINUTES * 60
    )
    return response


@private_api_router.post("/records/")
def create_record(record: Record, service: Service = Depends(get_service)) -> Record:
    return service.create_record(record)

@private_api_router.post("/records/backfill/")
def backfill_records(records: list[Record], service: Service = Depends(get_service)) -> list[Record]:
    return service.backfill_records(records)

@private_api_router.post("/records/insert/")
def insert_record(service: Service = Depends(get_service)) -> Record:
    return service.insert()

@private_api_router.get("/records/")
def read_records(filters: Filters = Depends(get_filters), service: Service = Depends(get_service)) -> list[Record]:
    return service.read_records(filters)

@private_api_router.get("/records/{record_id}")
def read_record(record_id: str, service: Service = Depends(get_service)) -> Record:
    return service.read_record_by_id(record_id)

@private_api_router.put("/records/{record_id}")
def update_record(record_id: str, record: Record, service: Service = Depends(get_service)) -> Record:
    return service.update_record(record_id, record)

@private_api_router.delete("/records/{record_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: str, service: Service = Depends(get_service)):
    service.delete_record(record_id)
    return ""
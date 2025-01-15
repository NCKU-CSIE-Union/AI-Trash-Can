from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Response, Form, status
from fastapi.responses import RedirectResponse

from src.schema import Record, Filters, LineChartRecord
from src.model import Service
from src.security import required_login, create_token
from src.config import server_config

public_api_router = APIRouter()
private_api_router = APIRouter(prefix="/api", dependencies=[Depends(required_login)])


def get_filters(
    seen: bool = None, created_at_start: int = None, created_at_end: int = None
):
    return Filters(
        seen=seen, created_at_start=created_at_start, created_at_end=created_at_end
    )


def get_service():
    return Service()


@public_api_router.get("/api/health/")
def health():
    return {"status": "ok"}


@public_api_router.post("/api/login/")
def login(
    response: Response,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    if (
        username != server_config.auth.USERNAME
        or password != server_config.auth.PASSWORD
    ):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    response = RedirectResponse(url="/data", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="auth",
        value=create_token(username),
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=server_config.auth.EXPIRE_MINUTES * 60,
    )
    return response


@private_api_router.post("/records/", response_model_by_alias=False)
def create_record(record: Record, service: Service = Depends(get_service)) -> Record:
    return service.create_record(record)


@private_api_router.post("/records/backfill/", response_model_by_alias=False)
def backfill_records(
    records: list[Record], service: Service = Depends(get_service)
) -> list[Record]:
    return service.backfill_records(records)


@private_api_router.post("/records/insert/", response_model_by_alias=False)
def insert_record(service: Service = Depends(get_service)) -> Record:
    return service.insert()


@private_api_router.get("/records/", response_model_by_alias=False)
def read_records(
    filters: Filters = Depends(get_filters), service: Service = Depends(get_service)
) -> list[Record]:
    return service.read_records(filters)


@private_api_router.get("/records/line/", response_model_by_alias=False)
def read_records_line_chart(
    aggregate_by: Literal["month", "day", "hour", "minute"] | None = "day",
    limit: int | None = 50,
    service: Service = Depends(get_service),
) -> list[LineChartRecord]:
    return service.read_records_line_chart(aggregate_by, limit)


@private_api_router.get("/records/heatmap/", response_model_by_alias=False)
def read_records_heatmap(
    aggregate_by: Literal["month", "day", "hour", "minute"] | None = "hour",
    service: Service = Depends(get_service),
) -> dict:
    return service.read_heat_maps(aggregate_by)


@private_api_router.get("/records/{record_id}", response_model_by_alias=False)
def read_record(record_id: str, service: Service = Depends(get_service)) -> Record:
    return service.read_record_by_id(record_id)


@private_api_router.put("/records/{record_id}", response_model_by_alias=False)
def update_record(
    record_id: str, record: Record, service: Service = Depends(get_service)
) -> Record:
    return service.update_record(record_id, record)


@private_api_router.delete(
    "/records/{record_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_record(record_id: str, service: Service = Depends(get_service)):
    service.delete_record(record_id)
    return ""

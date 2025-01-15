from datetime import timedelta

import datetime
import uuid
from jose import JWTError, jwt

from fastapi import Depends, status, HTTPException
from fastapi.security import APIKeyHeader, APIKeyCookie

from src.config import server_config


cookie_schema = APIKeyCookie(name="auth", auto_error=False)
header_schema = APIKeyHeader(name="api_key", auto_error=False)


async def required_login(
    token: str | None = Depends(cookie_schema),
    api_key: str | None = Depends(header_schema),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    if api_key == server_config.auth.API_KEY:
        return True
    if token is None:
        raise credentials_exception
    payload = decode_jwt(
        jwt_token=token,
        secret_key=server_config.auth.SECRET_KEY,
        algorithm=server_config.auth.ALGORITHM,
        issuer=server_config.auth.ISSUER,
    )

    if (payload is None) or ("sub" not in payload):
        raise credentials_exception
    return payload.get("sub")


def is_valid_token(token: str) -> bool:
    payload = decode_jwt(
        jwt_token=token,
        secret_key=server_config.auth.SECRET_KEY,
        algorithm=server_config.auth.ALGORITHM,
        issuer=server_config.auth.ISSUER,
    )

    return payload is not None and "sub" in payload


def create_token(sub: str) -> str:
    access_token_expires_at = get_now() + timedelta(
        minutes=server_config.auth.EXPIRE_MINUTES
    )
    return create_jwt(
        sub=sub,
        secret_key=server_config.auth.SECRET_KEY,
        algorithm=server_config.auth.ALGORITHM,
        issuer=server_config.auth.ISSUER,
        expires_at=access_token_expires_at,
    )


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_now_iso_8601_format() -> str:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()


def get_now_custom_gmt8_format() -> str:
    """
    - GMT+8
    - format: `yyyyMMddHHmmssSSS`
    """
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "000"


def get_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC).replace(microsecond=0)


def with_timezone(dt: datetime.datetime) -> datetime.datetime:
    return dt.replace(tzinfo=datetime.UTC)


def create_jwt(
    sub: str,
    expires_at: datetime.datetime,
    algorithm: str | None = None,
    secret_key: str | None = None,
    issuer: str | None = None,
    additional_claims: dict | None = None,
) -> str:
    signed_at = get_now()

    payload = {
        "exp": expires_at,
        "iat": signed_at,
        "nbf": signed_at,
        "sub": sub,
        "iss": issuer,
    }

    if additional_claims:
        payload.update(additional_claims)

    encoded_jwt = jwt.encode(claims=payload, key=secret_key, algorithm=algorithm)
    return encoded_jwt


def decode_jwt(
    jwt_token: str,
    algorithm: str | None = None,
    secret_key: str | None = None,
    issuer: str | None = None,
) -> dict:
    try:
        payload = jwt.decode(
            jwt_token,
            secret_key,
            algorithms=algorithm,
            issuer=issuer,
        )
        return payload
    except JWTError:
        return None

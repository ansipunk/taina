import secrets

import fastapi
import fastapi.security

from . import models
from . import security
from .core import config

OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="/api/tokens/obtain")


class AuthenticationError(Exception):
    pass


async def authenticate_user(username: str, password: str):
    try:
        user = await models.user_get(username)
    except models.UserDoesNotExist as e:
        raise AuthenticationError from e

    if not security.verify_password(password, user["password"]):
        raise AuthenticationError

    return user


async def create_refresh_token(
    username: str,
    ttl: int = config.security.refresh_token_ttl,
) -> str:
    refresh_token = secrets.token_urlsafe(48)
    return await models.refresh_token_set(username, refresh_token, ttl)


async def create_access_token(
    username: str,
    refresh_token: str,
    ttl: int = config.security.access_token_ttl,
) -> str:
    access_token = secrets.token_urlsafe(48)
    return await models.access_token_set(username, access_token, refresh_token, ttl)


async def get_current_user(access_token: str = fastapi.Depends(OAUTH2_SCHEME)):
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        username = await models.access_token_get(access_token)
    except models.TokenDoesNotExist:
        raise credentials_exception

    try:
        user = await models.user_get(username)
    except models.UserDoesNotExist:
        raise credentials_exception

    return user

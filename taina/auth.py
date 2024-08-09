import datetime

import fastapi
import fastapi.security
import jwt
import jwt.exceptions

from . import models
from . import security
from .core import config

ALGORITHM="HS256"
OAUTH2_SCHEME = fastapi.security.OAuth2PasswordBearer(tokenUrl="api/tokens/access")


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



def create_access_token(
    data: dict,
    ttl_minutes: int = config.security.access_token_ttl,
):
    expire = (
        datetime.datetime.now(datetime.timezone.utc) +
        datetime.timedelta(minutes=ttl_minutes)
    )
    data = {**data, "exp": expire}
    return jwt.encode(data, config.security.secret_key, algorithm=ALGORITHM)


async def get_current_user(token: str = fastapi.Depends(OAUTH2_SCHEME)):
    credentials_exception = fastapi.HTTPException(
        status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, config.security.secret_key, algorithms=[ALGORITHM])
    except jwt.exceptions.InvalidTokenError:
        raise credentials_exception

    username = payload.get("sub")

    if not username:
        raise credentials_exception

    try:
        user = await models.user_get(username)
    except models.UserDoesNotExist:
        raise credentials_exception

    return user

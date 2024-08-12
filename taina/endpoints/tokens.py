import fastapi
import fastapi.exceptions
import fastapi.security

from .. import auth
from .. import models
from .. import schemas

router = fastapi.APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("/obtain", response_model=schemas.Token)
async def obtain_token(
    form_data: fastapi.security.OAuth2PasswordRequestForm = fastapi.Depends(),
):
    try:
        user = await auth.authenticate_user(form_data.username, form_data.password)
    except auth.AuthenticationError:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    username = user["username"]
    refresh_token = await auth.create_refresh_token(username)
    access_token = await auth.create_access_token(username, refresh_token)

    return schemas.Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",  # noqa: S106
    )


@router.post("/refresh", response_model=schemas.Token)
async def refresh_token(refresh_token: str):
    try:
        username = await models.refresh_token_get(refresh_token)
    except models.TokenDoesNotExist:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect refresh token",
        )

    await models.refresh_token_del(refresh_token)

    new_refresh_token = await auth.create_refresh_token(username)
    new_access_token = await auth.create_access_token(username, new_refresh_token)

    return schemas.Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        token_type="bearer",  # noqa: S106
    )


@router.post("/revoke")
async def revoke_token(
    access_token: str | None = None,
    refresh_token: str | None = None,
):
    if not access_token and not refresh_token:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="One or both of access_token or refresh_token must be provided",
        )

    if access_token:
        dynamic_refresh_token = await models.refresh_token_get_by_access_token(
            access_token,
        )

        if dynamic_refresh_token:
            await models.refresh_token_del(dynamic_refresh_token)

    if refresh_token:
        await models.refresh_token_del(refresh_token)

import fastapi
import fastapi.exceptions
import fastapi.security

from .. import auth
from .. import schemas

router = fastapi.APIRouter(prefix="/tokens", tags=["tokens"])


@router.post("/access", response_model=schemas.Token)
async def obtain_access_token(
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

    access_token = auth.create_access_token(data={"sub": user["username"]})
    return schemas.Token(access_token=access_token, token_type="bearer")

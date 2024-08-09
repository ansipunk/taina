import fastapi
import fastapi.exceptions

from .. import auth
from .. import models
from .. import schemas

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserGet)
async def user_create(user: schemas.UserCreate):
    try:
        return await models.user_create(user)
    except models.UsernameInUse:
        raise fastapi.exceptions.HTTPException(400)


@router.get("/", response_model=schemas.UserList)
async def users_list():
    users = await models.user_list()
    return {"users": users}


@router.get("/me", response_model=schemas.UserGet)
async def read_users_me(current_user=fastapi.Depends(auth.get_current_user)):
    return current_user


@router.get("/{username}", response_model=schemas.UserGet)
async def users_get(username: str):
    try:
        return await models.user_get(username)
    except models.UserDoesNotExist:
        raise fastapi.exceptions.HTTPException(404)


@router.put("/{username}", response_model=schemas.UserGet)
async def users_update(username: str, user: schemas.UserUpdate):
    try:
        return await models.user_update(username, user)
    except models.UserDoesNotExist:
        raise fastapi.exceptions.HTTPException(404)


@router.delete("/{username}")
async def users_delete(username: str):
    await models.user_delete(username)
    raise fastapi.exceptions.HTTPException(204)

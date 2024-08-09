import pydantic

from .. import security


class User(pydantic.BaseModel):
    display_name: str | None = None


class UserCreate(User):
    username: str
    password: str

    @pydantic.field_validator("password", mode="after")
    @classmethod
    def hash_password(cls, password: str) -> str:
        return security.hash_password(password)


class UserUpdate(User):
    pass


class UserGet(User):
    username: str


class UserList(pydantic.BaseModel):
    users: list[UserGet]

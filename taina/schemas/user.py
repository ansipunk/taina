import pydantic


class User(pydantic.BaseModel):
    password: str


class UserCreate(User):
    username: str


class UserUpdate(User):
    pass


class UserGet(UserCreate):
    pass


class UserList(pydantic.BaseModel):
    users: list[UserGet]

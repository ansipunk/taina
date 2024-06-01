import pydantic


class User(pydantic.BaseModel):
    password: str


class UserCreate(User):
    username: str


class UserUpdate(User):
    pass

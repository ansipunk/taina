import pydantic

from .. import security


class User(pydantic.BaseModel):
    display_name: pydantic.constr(min_length=3, max_length=64) | None = None

    @pydantic.field_validator("display_name", mode="before")
    @classmethod
    def validate_display_name(cls, display_name: str) -> str:
        display_name = display_name.strip()

        if not display_name:
            raise ValueError("Empty display names are not allowed")

        for character in display_name:
            if not character.isalnum() and character != " ":
                raise ValueError("Only alphanumeric characters and spaces are allowed")

        return display_name


class UserCreate(User):
    username: pydantic.constr(min_length=3, max_length=64, strip_whitespace=True)
    password: pydantic.constr(min_length=8, max_length=128, strip_whitespace=True)

    @pydantic.field_validator("username", mode="before")
    @classmethod
    def validate_username(cls, username: str) -> str:
        for character in username:
            if not character.isalnum() or character.isupper():
                raise ValueError("Only lowercase characters and digits are allowed")

        return username

    @pydantic.field_validator("password", mode="before")
    @classmethod
    def check_password_strength(cls, password: str) -> str:
        has_numbers = False
        has_uppercase = False
        has_lowercase = False
        has_special_symbols = False

        for character in password:
            if has_numbers and has_uppercase and has_lowercase and has_special_symbols:
                break

            if character.isdigit():
                has_numbers = True
            elif character.isupper():
                has_uppercase = True
            elif character.islower():
                has_lowercase = True
            else:
                has_special_symbols = True

        if not has_numbers:
            raise ValueError("Password must have at least 1 digit")

        if not has_uppercase:
            raise ValueError("Password must have at least 1 uppercase character")

        if not has_lowercase:
            raise ValueError("Password must have at least 1 lowercase character")

        if not has_special_symbols:
            raise ValueError("Password must have at least 1 special symbol")

        return password

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

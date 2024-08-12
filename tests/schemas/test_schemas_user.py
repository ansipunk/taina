import pydantic
import pytest

import taina.schemas


def test_validate_username():
    taina.schemas.UserCreate(
        username="username10",
        password="P@ssw0rd",
    )


@pytest.mark.parametrize(
    ("username", "error_message"),
    [
        ("u", "String should have at least 3 characters"),
        ("u" * 65, "String should have at most 64 characters"),
        ("Username", "Only lowercase characters and digits are allowed"),
        ("user.name", "Only lowercase characters and digits are allowed"),
    ],
)
def test_validate_username_invalid(username: str, error_message: str):
    with pytest.raises(pydantic.ValidationError) as e:
        taina.schemas.UserCreate(
            username=username,
            password="P@ssw0rd",
        )

    assert error_message in str(e.value)


def test_validate_password():
    taina.schemas.UserCreate(
        username="username10",
        password="P@ssw0rd",
    )


@pytest.mark.parametrize(
    ("password", "error_message"),
    [
        ("P@s0", "String should have at least 8 characters"),
        ("P@s0" * 64, "String should have at most 128 characters"),
        ("p@ssw0rd", "Password must have at least 1 uppercase character"),
        ("P@SSW0RD", "Password must have at least 1 lowercase character"),
        ("P@ssword", "Password must have at least 1 digit"),
        ("Passw0rd", "Password must have at least 1 special symbol"),
    ],
)
def test_validate_password_invalid(password: str, error_message: str):
    with pytest.raises(pydantic.ValidationError) as e:
        taina.schemas.UserCreate(
            username="username10",
            password=password,
        )

    assert error_message in str(e.value)


def test_validate_display_name():
    taina.schemas.UserCreate(
        username="username10",
        password="P@ssw0rd",
        display_name="User Name",
    )


@pytest.mark.parametrize(
    ("display_name", "error_message"),
    [
        ("U", "String should have at least 3 characters"),
        ("U" * 128, "String should have at most 64 characters"),
        ("Usern@me", "Only alphanumeric characters and spaces are allowed"),
        ("  ", "Empty display names are not allowed"),
    ],
)
def test_validate_display_name_invalid(display_name: str, error_message: str):
    with pytest.raises(pydantic.ValidationError) as e:
        taina.schemas.UserCreate(
            username="username10",
            password="P@ssw0rd",
            display_name=display_name,
        )

    assert error_message in str(e.value)

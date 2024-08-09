import taina.security


def test_hash_and_verify_password():
    plain_password = "secret_password"
    hashed_password = taina.security.hash_password(plain_password)
    assert taina.security.verify_password(plain_password, hashed_password) is True


def test_verify_invalid_password():
    password_hash = taina.security.hash_password("valid password")
    assert taina.security.verify_password("invalid password", password_hash) is False

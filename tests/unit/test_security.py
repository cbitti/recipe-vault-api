from app.core import security


def test_password_hashing():
    password = "secret_password"
    hashed = security.get_password_hash(password)

    assert hashed != password
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrong_password", hashed)


def test_get_password_hash_is_deterministic_enough():
    # Ensure hashing the same password twice produces valid hashes
    # (Note: Argon2 salts randomly, so strings won't match, but both should verify)
    p = "test"
    h1 = security.get_password_hash(p)
    h2 = security.get_password_hash(p)
    assert security.verify_password(p, h1)
    assert security.verify_password(p, h2)

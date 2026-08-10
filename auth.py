import bcrypt


def hash_password(plain_password: str) -> str:
    plain_password_byte = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(plain_password_byte, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
from os import error
from argon2 import PasswordHasher
from fastapi import HTTPException

ph = PasswordHasher()


def hash_password(password: str) -> str:
    hashed = ph.hash(password)
    return hashed
    

def verify_password(password_hash, password_attempt):
    return ph.verify(password_hash, password_attempt)


    
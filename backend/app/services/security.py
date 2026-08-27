from os import error
from argon2 import PasswordHasher
from fastapi import HTTPException

ph = PasswordHasher()


def hash_password(password: str) -> str:
    hashed = ph.hash(password)
    return hashed
    

def verify_password(password_hash, password_attempt):
    return ph.verify(password_hash, password_attempt)
    
def issue_token(user_id: int):
    pass

    

# example_pass = "Password123"

# hashed_pass = hash_password(example_pass)
# pass_attempt = "Hey there"
# print(verify_password(hashed_pass, hash_password(pass_attempt)))
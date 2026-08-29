from datetime import datetime, timedelta, timezone
import jwt
from ..core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION_MINUTES = 30

def create_access_token(user_id: int):
    now = datetime.now(timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_DURATION_MINUTES)

    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM,

    )



def verify_access_token(token: str):
    
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM
    )

    return payload
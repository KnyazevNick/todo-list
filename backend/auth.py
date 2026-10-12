from datetime import datetime, timedelta, timezone
import jwt
from backend.config import settings



def create_access_token(user_id: int) -> str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(hours=1)

    key = settings.jwt_secret.get_secret_value()
    payload = {
        "sub": str(user_id),
        "exp": expires_at
    }

    token = jwt.encode(payload, key, algorithm="HS256")
    return token


def decode_access_token(token: str) -> dict | None:
    key = settings.jwt_secret.get_secret_value()
    try:
        payload = jwt.decode(
            token,
            key,
            algorithms=["HS256"],
            options={"require": ["sub", "exp"]},
        )

    except jwt.exceptions.InvalidTokenError:
        return None
    
    else:
        return payload
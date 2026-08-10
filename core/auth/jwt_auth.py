from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.models import TokenModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from core.config import settings

security = HTTPBearer()

def get_authenticated_user(credentials:HTTPAuthorizationCredentials = Depends(security),
                           db: Session = Depends(get_db)):
    return None

def generate_access_token(user_id: int, expires_in: int = 60*5) -> str:
    now = datetime.utcnow()
    payload = {
        "type": "access",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds = expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = "HS256")

def generate_refresh_token(user_id: int, expires_in: int = 3600*2) -> str:
    now = datetime.utcnow()
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": now,
        "exp": now + timedelta(seconds = expires_in)
    }
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm = "HS256")
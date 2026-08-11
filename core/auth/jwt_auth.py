from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from users.models import UserModel
from core.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError
from core.config import settings

security = HTTPBearer()

def get_authenticated_user(credentials:HTTPAuthorizationCredentials = Depends(security),
                           db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms = "HS256")
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "user_id is not in the payload")
        if decoded.get("type") != "access":
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "token type is not valid")
        if datetime.fromtimestamp(decoded.get("exp"))<datetime.utcnow():
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "token expired")
        user_obj = db.query(UserModel).filter_by(id = user_id).one()
    except InvalidSignatureError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Authentication failed, invalid signiture")
    except DecodeError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Authentication failed, decode failed")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = f"Authentication failed, {e}")
    return user_obj

def decode_refresh_token(token):
    try:
        decoded = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms = "HS256")
        user_id = decoded.get("user_id", None)
        if not user_id:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "user_id is not in the payload")
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "token type is not valid")
        if datetime.fromtimestamp(decoded.get("exp"))<datetime.utcnow():
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                                        detail = "Authentication failed, " \
                                        "token expired")
    except InvalidSignatureError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Authentication failed, invalid signiture")
    except DecodeError:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = "Authentication failed, decode failed")
    except Exception as e:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, 
                            detail = f"Authentication failed, {e}")
    return user_id

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
from fastapi import APIRouter, Depends, HTTPException, status, Path
from fastapi.responses import JSONResponse
from users.schemas import *
from users.models import UserModel, TokenModel
from auth.jwt_auth import generate_access_token, generate_refresh_token
from sqlalchemy.orm import Session
from core.database import get_db
import secrets

router = APIRouter (tags = ["users"], prefix = "/users")

def generate_token(length = 32):
     return secrets.token_hex(length)

@router.post("/login")
async def user_login(request: TaskLoginSchema, db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(user_name = request.user_name.lower()).first()
    if not user_obj:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                            detail = "user does not exist")
    if not user_obj.verify_password(request.password):
         raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, 
                                     detail = "password is invalid")
    '''token_obj = TokenModel(user_id = user_obj.id, token = generate_token())
    db.add(token_obj)
    db.commit()
    db.refresh(token_obj)'''
    access_token = generate_access_token(user_obj.id)
    refresh_token = generate_refresh_token(user_obj.id)
    return JSONResponse(content = {"detail" : "logged in seccessfully", 
                                   "access_token": access_token,
                                   "refresh_token": refresh_token})

@router.post("/register")
async def user_register(request: TaskRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(user_name = request.user_name.lower()).first():
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                                detail = "the username already exists")
    user_obj = UserModel(user_name = request.user_name.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    return JSONResponse(content = {"detail" : "user registered seccessfully"})

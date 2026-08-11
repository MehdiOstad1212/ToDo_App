from pydantic import BaseModel, Field, field_validator
from fastapi import HTTPException, status


class TaskLoginSchema(BaseModel):
    user_name: str = Field(..., max_length = 250, description = "username of the user")
    password: str = Field(..., description = "password of the user")


class TaskRegisterSchema(BaseModel):
    user_name: str = Field(..., max_length = 250, description = "username of the user")
    password: str = Field(..., description = "password of the user")
    password_confirm: str = Field(..., description = "confirmation of the password")

    @field_validator("password_confirm")
    def check_password_match (cls, password_confirm, validation):
        if (password_confirm != validation.data.get("password")):
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, 
                                            detail = "passwords are not match")
        return password_confirm

class UserRefreshTokenSchema(BaseModel):
    refresh_token: str = Field(..., description = "refresh token of the user")

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, constr, BeforeValidator, Field
from bson.objectid import ObjectId

PyObjectId = Annotated[str, BeforeValidator(str)]


class User(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserBaseSchema(User):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    created_at: datetime
    modified_at: datetime


class RegisteredUser(UserBaseSchema):
    password_hash: str


class CreateUserSchema(User):
    password: constr(min_length=8)


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserResponse(BaseModel):
    status: str
    user: User

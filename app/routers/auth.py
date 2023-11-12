from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Response, status, Depends, HTTPException, Header
from datetime import datetime, timedelta

from app.config.settings import settings
from app.schemas.user import CreateUserSchema, UserResponse, RegisteredUser, User, LoginUserSchema
from app.schemas.login import LoginResponse
from app.database.database import Users
from app.utils.password import hash_password, verify_password
from app.utils.oauth2 import create_refresh_token, create_access_token, auth_user, refresh_token

router = APIRouter()


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register(payload: CreateUserSchema):
    user = Users.find_one({'email': payload.email.lower()})

    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Account already exist'
        )
    now = datetime.utcnow()
    new_user = RegisteredUser(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        created_at=now,
        modified_at=now,
        password_hash=hash_password(payload.password)
    )
    Users.insert_one(new_user.model_dump(by_alias=True, exclude=['id']))
    return UserResponse(status="success", user=User(**new_user.model_dump()))


@router.post('/login', status_code=status.HTTP_202_ACCEPTED, response_model=LoginResponse)
async def login(payload: LoginUserSchema):
    user = Users.find_one({'email': payload.email.lower()})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    user = RegisteredUser(**user)
    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(
        hours=settings.ACCESS_TOKEN_EXPIRES_IN)
    refresh_token_expires = timedelta(
        days=settings.REFRESH_TOKEN_EXPIRES_IN)
    access_token = create_access_token(
        data={"user_id": str(user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"user_id": str(user.id)}, expires_delta=refresh_token_expires
    )

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/refresh')
async def refresh(new_bearer: str = Depends(refresh_token)):
    return {"token": new_bearer}


@router.get('/me')
async def me(user: RegisteredUser = Depends(auth_user)):
    """Example of protected route"""
    print(user)
    return User(**user.model_dump())

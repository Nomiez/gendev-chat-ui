from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import token_schema
from app.services.auth_service import get_access_token

router = APIRouter(
    prefix="/token",
    tags=['Token']
)


@router.post("/", response_model=token_schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    return {"access_token": get_access_token(user_credentials), "token_type": "bearer"}

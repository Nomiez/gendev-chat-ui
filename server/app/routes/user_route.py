from __future__ import annotations

from fastapi import status, HTTPException, Depends, APIRouter, UploadFile, File, Query
from starlette.responses import FileResponse

from app.schemas.user_schema import (
    UserGet,
    UserPost, UserSchema, UserGetFiltered,
)

from app.services import user_service, auth_service
from app.services.auth_service import is_valid_user
from app.utils.parser_utils import parse_list

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get("/{id}/image/", responses={200: {"content": {"image/png": {}}}}, response_class=FileResponse)
def get_image(id: int):
    print(f"media/profile_pictures/{user_service.get_user_by_id(int(id)).profile_picture}")
    return FileResponse(path=f"media/profile_pictures/{user_service.get_user_by_id(int(id)).profile_picture}")


@router.get("/{id}", response_model=UserGet)
async def get_user_by_id(id: int, user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    if user.user_id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
    return user


@router.get("/", response_model=list[UserGetFiltered])
async def get_user_by_keywords_paginated(keywords: list[str] = Depends(parse_list), page: int = Query(1), size: int = Query(5)):
    if len(keywords) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Keyword-List cannot be empty")
    return user_service.get_user_by_keyword_pag(keywords, page, size)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserGet)
async def create_user(user: UserPost):
    return user_service.create_user(user)


@router.post("/{id}/picture", response_model=UserGet)
async def upload(id: int, file: UploadFile = File(...),
                 user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    if user.user_id != id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized to access this resource")
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File format not supported")
    return user_service.save_profile_picture(user, file)

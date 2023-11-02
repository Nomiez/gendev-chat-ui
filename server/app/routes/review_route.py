from fastapi import APIRouter, Depends, Query, HTTPException
from enum import Enum

from starlette import status

from app.schemas.review_schema import ReviewSchema, ReviewPost, ReviewAverage
from app.schemas.user_schema import UserSchema
from app.services import auth_service
from app.services.auth_service import is_valid_user
from app.services.review_service import (
    get_review_assess_by_user_id_pag,
    get_reviews_written_by_user_id_pag,
    create_new_review,
    get_rating_by_user_id as get_rating
)

router = APIRouter(
    prefix="/review",
    tags=['Review']
)


class ReviewOption(Enum):
    FROM = "from"
    TO = "to"


@router.get("/user/{id}", response_model=ReviewSchema)
async def get_review_by_user_id_paginated(id: int, option: ReviewOption = Query("to"),
                                          page: int = Query(1),
                                          size: int = Query(5)):
    if option == ReviewOption.FROM:
        return get_reviews_written_by_user_id_pag(id, page, size)
    elif option == ReviewOption.TO:
        return get_review_assess_by_user_id_pag(id, page, size)
    else:
        raise HTTPException(status_code=400, detail="Invalid option")


@router.get("/user/{id}/rating", response_model=ReviewAverage)
async def get_rating_by_user_id(id: int):
    return get_rating(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ReviewSchema)
async def create_review(review: ReviewPost,  user: UserSchema | None = Depends(auth_service.get_current_user)):
    is_valid_user(user)
    return create_new_review(review, user)

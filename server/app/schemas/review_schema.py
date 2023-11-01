from pydantic import BaseModel
from app.schemas.user_schema import UserInReview, UserAttach


class ReviewSchema(BaseModel):
    review_id: int
    personal: int
    working: int
    payment: int
    text: str
    author: UserInReview


class ReviewAverage(BaseModel):
    personal: float
    working: float
    payment: float


class ReviewPost(BaseModel):
    personal: int
    working: int
    payment: int
    text: str
    user: UserAttach

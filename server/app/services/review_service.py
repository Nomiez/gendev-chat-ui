from app.schemas.review_schema import ReviewSchema, ReviewAverage, ReviewPost
from app.repositories.review_repository import review_repository
from app.schemas.user_schema import UserSchema


def get_review_assess_by_user_id_pag(user_id: int, page: int, size: int) -> list[ReviewSchema]:
    return review_repository.get_review_assess_by_user_id_pag(user_id, page, size)


def get_reviews_written_by_user_id_pag(user_id: int, page: int, size: int) -> list[ReviewSchema]:
    return review_repository.get_reviews_written_by_user_id_pag(user_id, page, size)


def get_rating_by_user_id(user_id: int) -> ReviewAverage:
    return review_repository.get_rating_by_user_id(user_id)


def create_new_review(review: ReviewPost, user: UserSchema) -> ReviewSchema:
    return review_repository.create_new_review(review, user)

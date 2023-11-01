from sqlalchemy import select, func

from app.models.reviews import Review
from app.schemas.review_schema import ReviewSchema, ReviewAverage
from app.schemas.user_schema import UserSchema
from app.utils.db import get_db


class ReviewRepository:
    def __init__(self):
        self.db = next(get_db())

    def get_review_assess_by_user_id_pag(self, user_id: int, page: int, size: int) -> list[ReviewSchema]:
        review_list = self.db.query(Review) \
            .filter(Review.user_id == user_id) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()
        res = []
        for review in review_list:
            res.append(ReviewSchema(**{**review.to_dict(), "author": review.author.to_dict()}))

        return res

    def get_reviews_written_by_user_id_pag(self, user_id: int, page: int, size: int) -> list[ReviewSchema]:
        review_list = self.db.query(Review) \
            .filter(Review.author_id == user_id) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()

        res = []
        for review in review_list:
            res.append(ReviewSchema(**{**review.to_dict(), "author": review.author.to_dict()}))

        return res

    def get_rating_by_user_id(self, user_id: int) -> ReviewAverage:
        review_list = self.db.query(
            func.avg(Review.personal).label("personal"),
            func.avg(Review.working).label("working"),
            func.avg(Review.payment).label("payment")
        ).filter(Review.user_id == user_id).first()

        return ReviewAverage(**review_list._asdict())

    def create_new_review(self, review: ReviewSchema, user: UserSchema) -> ReviewSchema:
        user_dict = review.model_dump()
        user_dict["user_id"] = user_dict["user"]["user_id"]
        user_dict["author_id"] = user.user_id
        user_dict.pop("user")
        new_review = Review(**user_dict)
        self.db.add(new_review)
        self.db.commit()
        self.db.refresh(new_review)
        return ReviewSchema(**{**new_review.to_dict(), "author": new_review.author.to_dict()})


review_repository = ReviewRepository()

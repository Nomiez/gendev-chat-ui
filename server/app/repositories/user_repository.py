from datetime import datetime
from typing import List

from pydantic import EmailStr

from app.schemas.user_schema import UserPut, UserPostExtended, UserSchema, UserPutExtended

from app.utils.db import get_db

from app.models import users, keywords, uk_links


class UserRepository:
    def __init__(self):
        self.db = next(get_db())

    def get_user_by_id(self, user_id: int) -> UserSchema:
        user = self.db.query(users.User).filter(users.User.user_id == user_id).first()
        if not user:
            raise Exception(f"User with id ${user_id} not found")
        keyword_list = user.keywords
        return UserSchema(**{**user.to_dict(), "keywords": [keyword.keyword for keyword in keyword_list]})

    def get_user_from_username(self, email: EmailStr) -> UserSchema:
        user = self.db.query(users.User).filter(users.User.email == email).first()
        # TODO Catch if user is None
        keyword_list = user.keywords
        if not user:
            raise Exception(f"User with username ${email} not found")
        return UserSchema(**{**user.to_dict(), "keywords": [keyword.keyword for keyword in keyword_list]})

    def get_user_from_keyword_pag(self, keyword_list: List, page: int, size: int) -> List[UserSchema]:
        user_list = self.db \
            .query(users.User) \
            .join(uk_links.UKLink) \
            .join(keywords.Keyword) \
            .filter(keywords.Keyword.keyword.in_(keyword_list)) \
            .offset((page - 1) * size) \
            .limit(size) \
            .all()

        return [UserSchema(**{**user.to_dict(), "keywords": [keyword.keyword for keyword in user.keywords]}) for user in
                user_list]

    def save_user(self, user: UserPostExtended) -> UserSchema:
        new_user = user.model_dump()
        new_user_keywords = new_user['keywords']
        new_user.pop('keywords')
        new_user = users.User(**new_user)
        for keyword in new_user_keywords:
            new_user.keywords.append(keywords.Keyword(keyword=keyword))
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        keyword_list = new_user.keywords
        return UserSchema(**{**new_user.to_dict(), "keywords": [keyword.keyword for keyword in keyword_list]})

    def update_user(self, user_id: int, user: UserPut) -> UserSchema:
        return self.update_user_internal(user_id, UserPutExtended(**user.model_dump()))

    def update_user_internal(self, user_id: int, user: UserPutExtended) -> UserSchema:
        old_user = self.get_user_by_id(user_id)
        if not old_user:
            raise Exception(f"User with id {user_id} not found")
        updated_values = user.model_dump(exclude_unset=True)
        for key, value in updated_values.items():
            setattr(old_user, key, value)
        user_dict = old_user.model_dump()
        user_dict.pop('keywords')
        new_user = users.User(**user_dict)
        new_user.updated_at = datetime.now()
        for keyword in user.keywords:
            new_user.keywords.append(keywords.Keyword(keyword=keyword))
        self.db.query(users.User).filter(users.User.user_id == user_id).update(new_user.to_dict())
        self.db.commit()
        return self.get_user_by_id(user_id)

    def remove_user(self, user):
        self.db.delete(user)
        self.db.commit()
        return user


user_repository = UserRepository()

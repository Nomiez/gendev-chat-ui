import os

from fastapi import UploadFile, HTTPException
from starlette import status

from app.schemas.user_schema import (
    UserPost,
    UserPostExtended,
    UserSchema, UserPutExtended
)
from app.repositories.user_repository import user_repository
from app.services import auth_service


def get_user_by_id(id: int) -> UserSchema:
    user = user_repository.get_user_by_id(id)
    return user


def get_user_by_email(email: str) -> UserSchema:
    user = user_repository.get_user_from_username(email)
    return user


def get_user_by_keyword_pag(keyword_list: list[str], page: int, size: int) -> list[UserSchema]:
    user_list = user_repository.get_user_from_keyword_pag(keyword_list, page, size)
    return user_list


def create_user(user: UserPost) -> UserSchema:
    salt = auth_service.generate_salt()
    hashed_password = auth_service.hash_password(user.password + salt)
    user.password = hashed_password
    user = UserPostExtended(**user.model_dump(), salt=salt, profile_picture="default.png")
    return user_repository.save_user(user)


def save_profile_picture(user: UserSchema, file: UploadFile) -> UserSchema:
    try:
        contents = file.file.read()
        new_filename = f"profile_picture_{user.user_id}" \
                       f"{'.jpg' if file.content_type == 'image/jpeg' else '.png'}"

        if user.profile_picture != "default.png":
            os.remove(f"media/profile_pictures/{user.profile_picture}")

        with open(f"media/profile_pictures/{new_filename}", "xb") as f:
            f.write(contents)
            user.profile_picture = new_filename
            return user_repository.update_user_internal(user.user_id, UserPutExtended(**user.model_dump()))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error saving file: {str(e)}")
    finally:
        file.file.close()

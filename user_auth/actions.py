# Django imports
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

# Python imports

# App imports
User = get_user_model()
from .exceptions import (
    InvalidUser,
    UserAlreadyExist,
    EmailAlreadyExist,
)
from .messages import (
    ERR_INVALID_USER,
    ERR_USERNAME_ALREADY_EXIST,
    ERR_EMAIL_ALREADY_EXIST,
)


def auth_user(user: User) -> dict:
    if not user:
        raise InvalidUser(detail=ERR_INVALID_USER)
    refresh = RefreshToken.for_user(user)
    user_data = {
        "pk": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
    }
    return {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "user": user_data,
    }


def register_user(username: str, password: str, email: str) -> User:
    user = User.objects.create(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


def check_does_username_exist(username: str) -> str:
    try:
        username = User.objects.get(username=username)
    except User.DoesNotExist:
        return username
    raise UserAlreadyExist(detail=ERR_USERNAME_ALREADY_EXIST)


def check_does_email_exist(email: str) -> str:
    try:
        email = User.objects.get(email=email)
    except User.DoesNotExist:
        return email
    raise EmailAlreadyExist(detail=ERR_EMAIL_ALREADY_EXIST)

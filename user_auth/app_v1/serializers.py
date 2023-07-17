# Django import
from rest_framework.serializers import Serializer, ModelSerializer, CharField
from django.contrib.auth import get_user_model, authenticate

# Python import

# App import
User = get_user_model()
from ..actions import (
    register_user,
    check_does_email_exist,
    check_does_username_exist,
)
from ..messages import (
    ERR_USERNAME_ALREADY_EXIST,
    ERR_EMAIL_ALREADY_EXIST,
    ERR_AUTH_FAILED,
)
from ..exceptions import UserAlreadyExist, EmailAlreadyExist, UserUnAuthorized


class RegisterUserSerializer(ModelSerializer):
    username = CharField(allow_blank=False, allow_null=False)
    password = CharField(allow_blank=False, allow_null=False, write_only=True)
    email = CharField(allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def validate_username(self, username):
        return check_does_username_exist(username=username)

    def validate_email(self, email):
        return check_does_email_exist(email=email)

    def create(self, validated_data):
        username = validated_data.get("username", None)
        password = validated_data.get("password", None)
        email = validated_data.get("email", None)
        return register_user(username=username, password=password, email=email)


class UserLoginSerializer(Serializer):
    username = CharField(allow_blank=True, allow_null=True)
    password = CharField(allow_blank=True, allow_null=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get("username", None)
        password = attrs.get("password", None)
        user = authenticate(username=username, password=password)
        if not user:
            raise UserUnAuthorized(detail=ERR_AUTH_FAILED)
        attrs["user"] = user
        return super().validate(attrs)


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
        ]

    def validate_username(self, username):
        return check_does_username_exist(username=username)

    def validate_email(self, email):
        return check_does_email_exist(email=email)

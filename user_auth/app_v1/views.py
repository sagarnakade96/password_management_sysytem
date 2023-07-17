# Django imports
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model

# Python imports

# App imports
from utils.generics import ActionViewSet
from .serializers import (
    RegisterUserSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
)
from ..actions import auth_user

User = get_user_model()


class UserRegisterAPI(ActionViewSet):
    permission_classes = [AllowAny]
    create_serializer = RegisterUserSerializer


class UserLoginAPI(ActionViewSet):
    permission_classes = [AllowAny]
    validate_serializer = UserLoginSerializer

    def action_validate(self, request, *args, **kwargs):
        self.action = "validate"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = auth_user(serializer.validated_data.get("user", None))
        return Response(user_data, status=status.HTTP_200_OK)


class UpdateUserAPI(ActionViewSet):
    update_serializer = UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()


user_registration = UserRegisterAPI.as_view({"post": "create"})
user_login = UserLoginAPI.as_view({"post": "action_validate"})
user_update = UpdateUserAPI.as_view({"post": "update"})

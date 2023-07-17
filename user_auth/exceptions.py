# Django imports
from rest_framework import (
    status,
    exceptions,
)


class InvalidUser(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class UserAlreadyExist(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EmailAlreadyExist(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class UserUnAuthorized(exceptions.APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

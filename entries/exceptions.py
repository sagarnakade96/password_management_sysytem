# Django imports
from rest_framework.exceptions import APIException
from rest_framework import status


class PinNotSet(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class CouldNotSetPin(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class InvalidPin(APIException):
    status_code = status.HTTP_400_BAD_REQUEST


class EntryDoesNotExist(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

# Django imports
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import get_user_model

# Python imports

# App imports
from .models import UserPin, Entries
from .exceptions import InvalidPin, EntryDoesNotExist
from .messages import ERR_INVALID_PIN, ERR_ENTRY_DOES_NOT_EXIST


User = get_user_model()


def set_user_pin(user: User, pin: str) -> bool:
    enc_pin = make_password(pin)
    user_pin_obj, _ = UserPin.objects.get_or_create(user=user, user_pin=enc_pin)
    if not user_pin_obj:
        return False
    return True


def __decrypt(user: User, app_name: str) -> str:
    try:
        entry_obj = Entries.objects.get(user=user, app_name=app_name)
    except Entries.DoesNotExist:
        raise EntryDoesNotExist(detail=ERR_ENTRY_DOES_NOT_EXIST)
    return entry_obj.decrypt_app_password


def show_app_password(user: User, app_name, pin: str) -> str:
    has_valid_pin = UserPin.objects.check_pin_for_user(user=user, pin=pin)
    if has_valid_pin:
        return __decrypt(user, app_name)
    raise InvalidPin(detail=ERR_INVALID_PIN)

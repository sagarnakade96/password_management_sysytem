# Django imports
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

# Python imports

# App imports
User = get_user_model()


class UserPinManager(models.Manager):
    def has_pin_set_for_user(self, user: User) -> bool:
        if self.get_queryset().filter(user=user).exists():
            return True
        return False

    def check_pin_for_user(self, user: User, pin: str) -> bool:
        obj = self.get_queryset().get(user=user)
        return check_password(pin, obj.user_pin)

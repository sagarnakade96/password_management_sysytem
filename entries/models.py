# Django imports
from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings

# Python imports
from cryptography.fernet import Fernet
import ast

# App imports
from .manager import UserPinManager
from .app_settings import AUTH_SALT

# Create your models here.
User = get_user_model()


class Entries(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    app_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="name set in the web while registration",
    )
    app_url = models.URLField(
        max_length=255,
        blank=True,
        null=True,
        help_text="url of the app of web",
    )
    app_username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="username set in a web or app",
    )
    app_email = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="email set in a web or app",
    )
    app_password = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="password set in a web or an app",
    )

    class Meta:
        verbose_name = "UserEntry"
        verbose_name_plural = "UserEntries"
        unique_together = ["user", "app_name", "app_url"]

    def __get_token(self):
        key = getattr(settings, AUTH_SALT, None)
        f = Fernet(key)
        return f

    @property
    def decrypt_app_password(self):
        f = self.__get_token()
        dec_pass = f.decrypt(ast.literal_eval(self.app_password))
        return dec_pass.decode("UTF-8")


class UserPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True, null=True)
    user_pin = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="set pin to verify the password",
    )

    class Meta:
        verbose_name = "UserPin"
        verbose_name_plural = "UserPins"

    objects = UserPinManager()

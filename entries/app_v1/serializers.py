# Django import
from rest_framework.serializers import (
    Serializer,
    ModelSerializer,
    CharField,
    SerializerMethodField,
    IntegerField,
)
from cryptography.fernet import Fernet
from django.conf import settings

# Python import

# App import
from ..models import Entries, UserPin
from utils.generics import UserHookSerializer
from ..exceptions import (
    PinNotSet,
    CouldNotSetPin,
    EntryDoesNotExist,
    InvalidPin,
)
from ..messages import (
    ERR_SET_PIN,
    ERR_COULD_NOT_SET_PIN,
    SUC_PIN_SET,
    ERR_ENTRY_DOES_NOT_EXIST,
    ERR_INVALID_PIN,
)
from ..actions import set_user_pin
from ..app_settings import AUTH_SALT


class EntrySerializer(UserHookSerializer, ModelSerializer):
    app_name = CharField(allow_blank=False, allow_null=False)
    app_url = CharField(allow_blank=False, allow_null=False)
    app_username = CharField(allow_blank=False, allow_null=False)
    app_email = CharField(allow_blank=False, allow_null=False)
    app_password = CharField(allow_blank=False, allow_null=False, write_only=True)

    class Meta:
        model = Entries
        fields = [
            "id",
            "user",
            "app_name",
            "app_url",
            "app_username",
            "app_email",
            "app_password",
        ]
        read_only_fields = ["user"]

    def __encrypt_password(self, password: str) -> str:
        key = getattr(settings, AUTH_SALT, None)
        f = Fernet(key)
        enc_pass = f.encrypt(password.encode())
        return enc_pass

    def validate_app_password(self, app_password):
        return self.__encrypt_password(password=app_password)

    def validate(self, attrs):
        user = self.get_user()
        has_pin = UserPin.objects.has_pin_set_for_user(user=user)
        if not has_pin:
            raise PinNotSet(detail=ERR_SET_PIN)
        attrs["user"] = user
        return super().validate(attrs)


class EntriesListSerializer(UserHookSerializer, ModelSerializer):
    class Meta:
        model = Entries
        fields = [
            "id",
            "app_name",
            "app_url",
        ]


class EntriesRetrieveSerializer(UserHookSerializer, ModelSerializer):
    app_id = CharField(write_only=True)
    user_pin = IntegerField(write_only=True)
    app_password = SerializerMethodField()

    class Meta:
        model = Entries
        fields = [
            "id",
            "app_id",
            "app_name",
            "app_url",
            "app_username",
            "app_email",
            "app_password",
            "user_pin",
        ]
        read_only_fields = [
            "app_name",
            "app_url",
            "app_username",
            "app_email",
            "app_password",
        ]

    def validate_app_id(self, app_id):
        try:
            self.instance = Entries.objects.get(id=app_id)
        except Entries.DoesNotExist:
            raise EntryDoesNotExist(detail=ERR_ENTRY_DOES_NOT_EXIST)

    def validate_user_pin(self, user_pin):
        user = self.get_user()
        if not UserPin.objects.check_pin_for_user(user=user, pin=user_pin):
            raise InvalidPin(detail=ERR_INVALID_PIN)

    def get_app_password(self, instance):
        return self.instance.decrypt_app_password


class SetPinSerializer(Serializer, UserHookSerializer):
    user_pin = CharField()

    def save(self, **kwargs):
        user = self.get_user()
        user_pin = self.validated_data.get("user_pin", None)
        set_pin = set_user_pin(user=user, pin=user_pin)
        if not set_pin:
            raise CouldNotSetPin(detail=ERR_COULD_NOT_SET_PIN)
        return SUC_PIN_SET, 200

# Django imports
from rest_framework.response import Response
from rest_framework import status

# Python imports

# App imports
from utils.generics import ActionViewSet
from .serializers import (
    EntriesListSerializer,
    EntrySerializer,
    SetPinSerializer,
    EntriesRetrieveSerializer,
)
from ..models import Entries


class EntriesView(ActionViewSet):
    list_serializer = EntriesListSerializer
    create_serializer = EntrySerializer
    validate_serializer = EntriesRetrieveSerializer

    def get_queryset(self):
        return Entries.objects.all()

    def action_validate(self, request, *args, **kwargs):
        self.action = "validate"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"detail": serializer.data}, status.HTTP_200_OK)


class SetPinView(ActionViewSet):
    save_serializer = SetPinSerializer


user_entries = EntriesView.as_view({"get": "list", "post": "create"})
user_entry_detail = EntriesView.as_view({"post": "action_validate"})
set_pin = SetPinView.as_view({"post": "action_save", "put": "update"})

# Django imports
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.status import HTTP_200_OK


# Python imports

# App imports


class UserHookSerializer:
    def get_request(self):
        """Retrieve request from serializer context

        Returns:
            Request: request object from serializer
        """
        return self.context.get("request", None)

    def get_user(self):
        """Retrieve logged in user from the request available in the serializer context

        Raises:
            NotFound: If request not available in context
            NotFound: IF request does not have user attribute

        Returns:
            User: Logged-in user's instance
        """
        request = self.get_request()
        if not request:
            raise NotFound("User is not available")
        if not hasattr(request, "user"):
            raise NotFound("User is not available")
        return request.user


class ActionViewSet(ModelViewSet):
    """Generic action view set to encapsulate additional operation support along with the normal CRUD operations.

    Adds supports for below additional operations:
    - save: To to used to modify the objects in conjunction with update
    - add: To be used to add the additional relationship to objects
    - remove: To be used to remove existing relationships the objects.


    Returns:
     Response: JSON response for the operations along with status and necessary headers as per REST API standards
    """

    list_serializer = None
    create_serializer = None
    retrieve_serializer = None
    update_serializer = None
    delete_serializer = None
    save_serializer = None
    add_serializer = None
    remove_serializer = None
    validate_serializer = None
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        attr = f"{self.action}_serializer"
        assert hasattr(self, attr) is not None, (
            "'%s' should either include a `%s` attribute,"
            "or override the `get_serializer_class` method."
            % (self.__class__.name__, attr)
        )
        return getattr(self, attr)

    def generate_response(self, data, status):
        return Response({"detail": data}, status)

    def create(self, request, *args, **kwargs):
        self.action = "create"
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        self.action = "list"
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.action = "retrieve"
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.action = "update"
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.action = "destroy"
        return super().destroy(request, *args, **kwargs)

    def action_add(self, request, *args, **kwargs):
        self.action = "add"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data, status = serializer.save()
        return self.generate_response(data, status)

    def action_save(self, request, *args, **kwargs):
        self.action = "save"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data, status = serializer.save()
        return self.generate_response(data, status)

    def action_remove(self, request, *args, **kwargs):
        self.action = "remove"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data, status = serializer.save()
        return self.generate_response(data, status)

    def action_validate(self, request, *args, **kwargs):
        self.action = "validate"
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.generate_response(serializer.data, status=HTTP_200_OK)

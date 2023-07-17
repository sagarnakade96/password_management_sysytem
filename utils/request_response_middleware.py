# Django imports
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone

# Python imports
import json
from http import HTTPStatus

# App imports
from utils.json_responses import JSONResponse


class RequestResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request = self.process_request(request)
        response = self.get_response(request)
        response = self.process_response(response)
        return response

    def process_request(self, request):
        return request

    def process_response(self, response):
        response_data = None
        if isinstance(response, JSONResponse):
            return response
        response_content_type = response.get("content-type", "")
        if response_content_type == "application/json":
            response_data = response.data if hasattr(response, "data") else ""
            http_code_to_message = {v.value: v.description for v in HTTPStatus}
            server_time = timezone.now()
            if response.status_code < 400:
                response.data = {
                    "code": response.status_code,
                    "message": http_code_to_message[response.status_code],
                    "data": response_data,
                    "error": None,
                    "server_time": server_time,
                }
            elif response.status_code >= 400:
                response.data = {
                    "code": response.status_code,
                    "message": http_code_to_message[response.status_code],
                    "error": response.data,
                    "data": None,
                    "server_time": server_time,
                }
            response.content = json.dumps(response.data, cls=DjangoJSONEncoder)
        return response

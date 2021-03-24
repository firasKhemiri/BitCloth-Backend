import functools
import json
import logging

from django.core.exceptions import ValidationError
from graphql.error import GraphQLError

logger = logging.getLogger(__name__)


class ResponseError(Exception):
    def __init__(self, message: str, code: str = None, params: dict = None):
        super().__init__(message)
        self.message = str(message)
        self.code = code
        self.params = params


class APIError(Exception):
    def __init__(self, message, response_data=None, status_code=None):
        self.status_code = status_code
        self._response_data = json.loads(response_data) if response_data else None
        super().__init__(message)

    @property
    def response_data(self):
        return self._response_data

    @response_data.setter
    def response_data_setter(self, value):
        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                # Response was not json-formatted, thus the value needs no transforming
                pass
        self._response_data = value


class ApiTimeoutException(APIError):
    MESSAGE = 'Connection failed, please try again later.'

    def __init__(self, message=None, response_data=None, status_code=None):
        if not message:
            message = self.MESSAGE
        super().__init__(message=message, response_data=response_data, status_code=status_code)


class PortalApiTimeoutException(ApiTimeoutException):
    pass


class QuoteApiTimeoutException(ApiTimeoutException):
    pass


class PgrTimeoutException(ApiTimeoutException):
    pass


class AuthenticationError(APIError):
    default_message = "Authentication failed."


class ExceptionBase(Exception):
    MESSAGE = "Internal Server Error."

    def __init__(self, message=None, *args):
        super().__init__(message or self.MESSAGE, *args)


class ValidationErrorBase(ValidationError):
    MESSAGE = "Invalid data."

    def __init__(self, message=None, *args):
        super().__init__(message or self.MESSAGE, *args)


class PoliciesFromDifferentUsersException(ExceptionBase):
    pass


class InvalidAmountOfPoliciesException(ExceptionBase):
    MESSAGE = "Invalid amount of policies"


class PGPEncryptionException(ExceptionBase):
    pass


class PGPDecryptionException(ExceptionBase):
    pass

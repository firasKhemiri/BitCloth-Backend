from xmlrpc.client import ResponseError

from django.core.exceptions import ValidationError, SuspiciousOperation
from django.http import HttpResponse
from graphene_django.views import GraphQLView
from graphql import GraphQLError
from graphql_jwt.exceptions import JSONWebTokenExpired, JSONWebTokenError

from common.exceptions import APIError


class ExceptionHandledGraphQLView(GraphQLView):
    """
    The default GraphQLView grabs all exceptions within the schema
    and displays it to the client, which is absurd.
    This class provides better handling of exceptions, only allowing
    a few selected exception-classes to get through to the schema output.

    https://github.com/graphql-python/graphene-django/issues/124
    """

    def execute_graphql_request(self, *args, **kwargs):
        # The super class will grab all errors in the result
        result = super().execute_graphql_request(*args, **kwargs)

        if getattr(result, "errors", False):
            for error in result.errors:
                try:
                    # Raise the original error to be caught on
                    # the exception blocks
                    if hasattr(error, "original_error"):
                        raise error.original_error

                    if isinstance(error, Exception):
                        raise error

                    raise Exception("Could not determine the exception type")
                except (
                    ValidationError,
                    GraphQLError,
                    SuspiciousOperation,
                    ResponseError,
                    JSONWebTokenExpired,
                    JSONWebTokenError
                ):
                    # These classes are allowed to get through w/o Sentry logging
                    continue

        return result

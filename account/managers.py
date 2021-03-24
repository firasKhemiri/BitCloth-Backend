from calendar import timegm
from datetime import datetime

from django.core import serializers
from graphql_jwt.settings import jwt_settings

from account.models import User
from account.models.serializers import UserSerializer


def follow_user(user: User):
    user.followers.add()


def jwt_payload_handler(user, context=None):
    username = user.get_username()

    if hasattr(username, 'pk'):
        username = username.pk
    payload = {
        'User': UserSerializer(instance=user).data,
        user.USERNAME_FIELD: username,
        'exp': datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA,
    }

    if jwt_settings.JWT_ALLOW_REFRESH:
        payload['origIat'] = timegm(datetime.utcnow().utctimetuple())

    if jwt_settings.JWT_AUDIENCE is not None:
        payload['aud'] = jwt_settings.JWT_AUDIENCE

    if jwt_settings.JWT_ISSUER is not None:
        payload['iss'] = jwt_settings.JWT_ISSUER

    return payload
from datetime import datetime

import facebook
import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.shortcuts import get_token

from account.models import  User
from account.schema_types import UserType


# class CreateUser(graphene.Mutation):
#     user = graphene.Field(UserType)
#     token = graphene.String()
#     refresh_token = graphene.String()
#
#     class Arguments:
#         username = graphene.String(required=True)
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)
#
#     def mutate(self, info, username, password, email):
#         user = get_user_model()(
#             username=username,
#             email=email,
#         )
#         user.set_password(password)
#         user.save()
#
#         token = get_token(user)
#         refresh_token = create_refresh_token(user)
#
#         return CreateUser(user=user, token=token, refresh_token=refresh_token)
#

class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    access_token = graphene.String()

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        access_token = graphene.String(required=True)

    def mutate(self, info, username, password, access_token):
        try:
            graph = facebook.GraphAPI(access_token=access_token)
            user_info = graph.get_object(
                id='me',
                fields='first_name, last_name, id, '
                       'email, gender, picture.type(large),'
                       ' birthday')
        except facebook.GraphAPIError:
            return JsonResponse({'error': 'Invalid data'}, safe=False)

        return CreateUser(access_token=access_token)


class AuthUserFB(graphene.Mutation):
    user = graphene.Field(UserType)
    token = graphene.String()
    refresh_token = graphene.String()
    class Arguments:
        access_token = graphene.String(required=True)

    def mutate(self, info, access_token):
        try:
            graph = facebook.GraphAPI(access_token=access_token)
            user_info = graph.get_object(
                id='me',
                fields='first_name, last_name, id, '
                       'email, gender, picture.type(large),'
                       ' birthday')
        except facebook.GraphAPIError:
            return JsonResponse({'error': 'Invalid data'}, safe=False)

        try:
            user = User.objects.get(facebook_id=user_info.get('id'))

        except User.DoesNotExist:
            password = User.objects.make_random_password()
            user = get_user_model()(
                first_name=user_info.get('first_name'),
                last_name=user_info.get('last_name'),
                email=user_info.get('email')
                      or '{0} without email'.format(user_info.get('last_name')),
                facebook_id=user_info.get('id'),
                picture=user_info.get('picture')['data']['url'],
                date_joined=datetime.now(),
                username=user_info.get('email') or user_info.get('last_name'),
                gender="MALE",
                is_active=1)
            user.is_complete = False
            user.set_password(password)
            user.save()

        token = get_token(user)
        refresh_token = create_refresh_token(user)

        return AuthUserFB(user=user, token=token, refresh_token=refresh_token)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    # creator = graphene.Field(CreatorType, id=graphene.Int())
    users = graphene.List(UserType)
    # creators = graphene.List(CreatorType)

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_user(self, info, **kwargs):
        user_id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=user_id)

        return None

    # def resolve_creator(self, info, **kwargs):
    #     id = kwargs.get('id')
    #
    #     if id is not None:
    #         return Creator.objects.get(pk=id)
    #
    #     return None
    #
    # def resolve_creators(self, info, **kwargs):
    #     return Creator.objects.all()


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

    # create_user = CreateUser.Field()
    auth_user_facebook = AuthUserFB.Field()

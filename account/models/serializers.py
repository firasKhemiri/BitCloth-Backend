from rest_framework import serializers

from account.models import User


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    coverPicture = serializers.CharField(source='cover_picture')
    # username = serializers.CharField(source='username')
    # username = serializers.CharField(source='username')


    class Meta:
        model = User
        # fields = '__all__'
        exclude = ['first_name','last_name','password','cover_picture']


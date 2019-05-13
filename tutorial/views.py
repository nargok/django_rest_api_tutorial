from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone

class TokenUserTypeOneSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username
        token['user_one'] = user.id
        token['start_datetime'] = timezone.now

        return token

class TokenUserTypeOneView(TokenObtainPairView):
    serializer_class = TokenUserTypeOneSerializer


class TokenUserTypeTwoSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username
        token['user_two'] = user.id
        token['user_two_action'] = 'get_list'
        token['start_datetime'] = timezone.now


        return token

class TokenUserTypeTwoView(TokenObtainPairView):
    serializer_class = TokenUserTypeTwoSerializer

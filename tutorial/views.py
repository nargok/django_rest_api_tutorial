from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.utils import timezone
from datetime import timedelta
from calendar import timegm

class TokenUserTypeOneSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username
        token['user_one'] = user.id

        # 有効日時をoverride
        now = timezone.now()
        expired = now + timedelta(minutes=10)
        token['start_datetime'] = timegm(now.utctimetuple())
        token['exp'] = timegm(expired.utctimetuple())

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

        # 有効日時をoverride
        now = timezone.now()
        expired = now + timedelta(minutes=15)
        token['start_datetime'] = timegm(now.utctimetuple())
        token['exp'] = timegm(expired.utctimetuple())

        return token

class TokenUserTypeTwoView(TokenObtainPairView):
    serializer_class = TokenUserTypeTwoSerializer

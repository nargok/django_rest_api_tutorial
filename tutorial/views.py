from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.utils import datetime_to_epoch
from django.utils import timezone
from datetime import timedelta
from calendar import timegm



class TokenForUserSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(TokenForUserSerializer, self).validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)

        access = refresh.access_token
        # 生存期間を変更する処理を実施する
        access.payload['exp'] = datetime_to_epoch(access.current_time + timedelta(minutes=15))
        # 現在時刻を設定 // 検証用項目
        access['start_datetime'] = timegm(access.current_time.utctimetuple())
        data['access'] = str(access)

        return data

    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)
    #
    #     token['name'] = user.username
    #     token['user_one'] = user.id
    #
    #     logger = logging.getLogger('development')
    #     logger.info("START DEBUGGING")
    #
    #     # 有効日時をoverride
    #     now = timezone.now()
    #     expired = now + timedelta(minutes=10)
    #     token['start_datetime'] = timegm(now.utctimetuple())
    #     token['exp'] = timegm(expired.utctimetuple())
    #
    #     logger.info("END DEBUGGING")
    #
    #     return token

class TokenForUserView(TokenObtainPairView):
    serializer_class = TokenForUserSerializer


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

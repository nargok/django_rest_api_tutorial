from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.utils import datetime_to_epoch
from django.utils import timezone
from datetime import timedelta
from calendar import timegm
from rest_framework import serializers, exceptions


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


from rest_framework_simplejwt.serializers import PasswordField
from django.contrib.auth import authenticate

class TokenUserTypeTwoSerializer(TokenObtainPairSerializer):
    # User = get_user_model()
    # username_field = User.USERNAME_FIELD

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

        # override start (\( ⁰⊖⁰)/)
        self.fields['app_id'] = serializers.CharField()
        # override end

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        # override start (\( ⁰⊖⁰)/)
        # 本来は、生徒に付与されたサービスと、入力IDの紐付けを
        if attrs['app_id'] != 'ENGLISH':
            print('項目は入れられるヽ(•̀ω•́ )ゝ')
            # raise exceptions.AuthenticationFailed(
            #     self.error_messages['not allowed service!!'],
            #     'no_active_account',
            # )
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        # override end  ٩( 'ω' )و

        return {}

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

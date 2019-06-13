from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView


User = get_user_model()

# ログインAPI用のSerializerその1
class MyTokenObtainSerializer(serializers.Serializer):
    username_field = User.USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

        # override start (\( ⁰⊖⁰)/)
        self.fields['app_id'] = serializers.CharField()
        # override end  ٩( 'ω' )و

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
            raise exceptions.PermissionDenied(detail="app_id is not correct. Please confirm.")
        # override end  ٩( 'ω' )و

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


# ログインAPI用のSerializerその2
class MyTokenObtainPairSerializer(MyTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data

# ログインAPI用のView
class MyLoginView(TokenObtainPairView):
    """
    ログイン認証用API
    """
    serializer_class = MyTokenObtainPairSerializer


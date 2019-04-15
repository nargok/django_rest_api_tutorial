from rest_framework import viewsets, permissions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import UserSerializer
from django.contrib.auth.models import User

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated,)
  # TODO認証クラスを変更する
  authentication_classes = (JSONWebTokenAuthentication,)

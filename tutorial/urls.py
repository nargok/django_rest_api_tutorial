"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
    TokenObtainSlidingView,
    TokenRefreshSlidingView
)
from rest_framework_swagger.views import get_swagger_view
from sample_app.views import MyTokenObtainPairView
from tutorial.views import TokenForUserView, TokenUserTypeTwoView

# hackしたView
from .hacked_view import MyLoginView, MyTokenRefreshView

schema_view = get_swagger_view(title='Pastebin API')

urlpatterns = [
    url(r'^', include('snippets.urls')),
    # 認証フレームワークを変更する
    # スライドトークンの実験
    url(r'^api/token/$', MyLoginView.as_view(), name='token_obtain_pair'),
    # url(r'^api/token/$', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # url(r'^api/token/$', TokenObtainSlidingView.as_view(), name='token_obtain_pair'),
    url(r'^api/token/verify/$', TokenVerifyView.as_view(), name='token_verify'),
    # スライドトークンの実験
    url(r'^api/token/refresh/$', MyTokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^api/token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),
    # url(r'^api/token/refresh/$', TokenRefreshSlidingView.as_view(), name='token_refresh'),

    # 認証トークンをカスタマイズする
    url(r'^api/token/user_type_one/$', TokenForUserView.as_view(), name='token_obtain_type_one'),
    url(r'^api/token/user_type_two/$', TokenUserTypeTwoView.as_view(), name='token_obtain_type_two'),
    url(r'^sample_app', include('sample_app.urls')),
    url(r'^docs', schema_view),
]

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]

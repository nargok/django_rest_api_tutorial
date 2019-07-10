from rest_framework import viewsets
from rest_framework import generics, permissions, renderers

from rest_framework.decorators import api_view, detail_route
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from snippets.models import Snippet, Tag
from snippets.serializers import SnippetSerializer, UserSerializer, TagSerializer
from snippets.permissions import IsOwnerOrReadOnly

from django.contrib.auth.models import User

class SnippetViewSet(viewsets.ModelViewSet):
  """
  This viewset automatically provides list, create, retrieve,
  update, destroy actions.
  """
  queryset = Snippet.objects.all()
  serializer_class = SnippetSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                        IsOwnerOrReadOnly,)

  @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
  def highlight(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)

  def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

class TagViewSet(viewsets.ModelViewSet):
  queryset = Tag.objects.all()
  serializer_class = TagSerializer
  permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

  def filter_queryset(self, queryset):
    queryset = Tag.objects.all()
    text_params = self.request.query_params.get('text', None)
    if text_params is not None:
      queryset = queryset.filter(text__contains=text_params)
    return queryset

class UserViewSet(viewsets.ReadOnlyModelViewSet):
  """
  This viewset automatically provides list and detail actions.
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

@api_view(['GET'])
def api_root(request, format=None):
  return Response({
    'users': reverse('user-list', request=request, format=format),
    'snippets': reverse('snippet-list', request=request, format=format),
  })

class SnippetHighlight(generics.GenericAPIView):
  queryset = Snippet.objects.all()
  renderer_classes = (renderers.StaticHTMLRenderer)

  def get(self, request, *args, **kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)

from snippets.tests.access_google import sample

class MockTestAPIView(APIView):
  def get(self, request):
    response = sample()
    return Response({
      'text': 'hello',
      'statusCodeFromGoogle': response['statusCode'],
      'ipFromGoogle': response['ip']
      })

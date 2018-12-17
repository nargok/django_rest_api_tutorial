from rest_framework import serializers
from snippets.models import Snippet, Tag, LANGUAGE_CHOICES, STYLE_CHOICES

from django.contrib.auth.models import User

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
  owner = serializers.ReadOnlyField(source='owner.username')
  highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

  class Meta:
    model = Snippet
    fields = ('url', 'id', 'highlight', 'owner',
              'title', 'code', 'linenos', 'language', 'style')

  def create(self, validated_data):
    """
    Create a new Snippet
    """
    return Snippet.objects.create(**validated_data)

  def update(self, instance, validated_data):
    """
    Update an existing Snippet instance
    """

    instance.title = validated_data.get('title', instance.title)
    instance.code = validated_data.get('code', instance.code)
    instance.linenos = validated_data.get('linenos', instance.linenos)
    instance.language = validated_data.get('language', instance.language)
    instance.style = validated_data.get('style', instance.style)
    instance.save()
    return instance

class TagSerializer(serializers.HyperlinkedModelSerializer):
  class Meta:
    model = Tag
    fields = ('url', 'id', 'text', 'snippets')

  def create(self, validated_data):
    """
    Create a new Tag
    """
    snippets_data = validated_data.pop('snippets')
    tag = Tag.objects.create(**validated_data)
    tag.save()

    for snippet_data in snippets_data:
      snippet = Snippet.objects.get(pk=snippet_data.id)
      if snippet:
        tag.snippets.add(snippet)

    return tag

  def update(self, instance, validated_data):
    """
    Update an existing Tag instance
    """
    instance.text = validated_data.get('text', instance.text)
    instance.save()
    return instance

class UserSerializer(serializers.HyperlinkedModelSerializer):
  snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

  class Meta:
    model = User
    fields = ('url', 'id', 'username', 'snippets',)

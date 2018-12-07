from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


class SnippetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Snippet
    fields = ('id', 'title', 'code', 'linenos', 'language', 'style')

  def create(self, validated_data):
    """
    Create a new Snippet
    :param validated_data:
    :return: a new Snippet instance,
    """
    return Snippet.objects.create(**validated_data)

  def update(self, instance, validated_data):
    """
    Update an existing Snippet instance
    :param instance:
    :param validated_data:
    :return: Updated an existingSnippet instance
    """
    instance.title = validated_data.get('title', instance.title)
    instance.code = validated_data.get('code', instance.code)
    instance.linenos = validated_data.get('linenos', instance.linenos)
    instance.language = validated_data.get('language', instance.language)
    instance.style = validated_data.get('style', instance.style)
    instance.save()
    return instance
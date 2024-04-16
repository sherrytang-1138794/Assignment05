from .models import Bookmark, Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User
from rest_framework import serializers


class BookmarkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bookmark
        fields = ("id", "title", "url", "notes", "date_added")


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        # owner = serializers.ReadOnlyField(source="owner.username")
        fields = ["id", "title", "code", "linenos", "language", "style", "owner"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField #add using CharField instead of CharField(write_only) for testing purpose 
    snippets = serializers.PrimaryKeyRelatedField(
        read_only=True,
        many=True, 
        #queryset=Snippet.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "snippets"]

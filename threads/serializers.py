from rest_framework import serializers
from threads.models import Thread, Post


class ThreadCreateSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Thread
        fields = ["id", "category", "title", "author", "createdAt"]


class ThreadListSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Thread
        fields = ["id", "category", "title", "author", "createdAt"]

    def get_author(self, obj):
        return obj.author.username


class PostSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Post
        fields = ['author', 'text', 'createdAt']

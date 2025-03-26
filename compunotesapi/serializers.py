from rest_framework import serializers
from .models import User, Tag, Rating, File, FileTag


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name']

class RatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating

class FileTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTag
        fields = ['tag_id', 'file_id']

class FileSerializer(serializers.ModelSerializer):
    tags = FileTagSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = ['id', 'path', 'tags']

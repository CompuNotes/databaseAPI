from rest_framework import serializers
from .models import User, Tag, Rating, File


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

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id', 'path', 'tags']

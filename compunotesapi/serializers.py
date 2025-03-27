from rest_framework import serializers
from .models import User, Tag, Rating, File


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, allow_blank=False)
    password = serializers.CharField(max_length=255, allow_blank=False, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

class TagSerializer(serializers.ModelSerializer):
    files = serializers.SlugRelatedField(many=True, read_only=True, slug_field='id')

    class Meta:
        model = Tag
        fields = ['id', 'name', 'files']

class FileSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    rating = serializers.SerializerMethodField()
    path = serializers.FilePathField(path='/home/compunotes/files', recursive=True)

    class Meta:
        model = File
        fields = ['id', 'title', 'path', 'user', 'tags', 'rating']

    def get_rating(self, obj):
        ratings = Rating.objects.filter(file_id=obj.id)
        if ratings:
            return sum([rating.rating for rating in ratings]) / len(ratings)
        return 0

class UploadSerializer(serializers.ModelSerializer):
    file_uploaded = serializers.FileField()

    class Meta:
        model = File
        fields = ['file_uploaded', 'title', 'user', 'tags']

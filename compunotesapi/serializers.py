from email.policy import default

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
    id = serializers.IntegerField(read_only=True)
    tags = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Tag.objects.all())
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    rating = serializers.SerializerMethodField(read_only=True)
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ['id', 'title', 'file', 'user', 'tags', 'rating']

    def get_rating(self, obj):
        ratings = Rating.objects.filter(file_id=obj.id)
        if ratings:
            return sum([rating.rating for rating in ratings]) / len(ratings)
        return 0

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        file = File.objects.create(**validated_data)
        file.tags.set(tags)
        return file

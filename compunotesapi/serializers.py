from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User, Tag, Rating, File

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        password = validated_data.pop('password')
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if 'password' in validated_data:
            user.set_password(password)
            user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

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

from django.shortcuts import render
import statistics
from rest_framework import viewsets

# Create your views here.
from django.http import HttpResponse

from .models import User, File, Tag
from .serializers import UserSerializer, FileSerializer, TagSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        username = self.request.query_params.get('username')
        if id is not None:
            queryset = User.objects.filter(id=id)
            return queryset
        elif username is not None:
            queryset = User.objects.filter(username=username)
            return queryset
        else:
            return User.objects.all()

class FileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FileSerializer

    def get_queryset(self):
        id = self.request.query_params.get('id')
        tag = self.request.query_params.get('tags')
        if id is not None:
            queryset = File.objects.filter(id=id)
            return queryset
        elif tag is not None:
            queryset = File.objects.filter(tag=tag)
            return queryset
        else:
            return File.objects.all()

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_queryset(self):
        id = self.request.query_params.get('id')
        name = self.request.query_params.get('name')
        if id is not None:
            queryset = Tag.objects.filter(id=id)
            return queryset
        elif name is not None:
            queryset = Tag.objects.filter(name=name)
            return queryset
        else:
            return Tag.objects.all()
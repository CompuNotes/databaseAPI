from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import File, Tag
from .serializers import UserSerializer, FileSerializer, TagSerializer

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FileViewSet(viewsets.ModelViewSet):
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

    def create(self, request):
        file_uploaded = request.FILES.get('file_uploaded')
        content_type = file_uploaded.content_type
        response = "POST API and you have uploaded a {} file".format(content_type)
        return Response(status=204)

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
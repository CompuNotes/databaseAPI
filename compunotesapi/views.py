from rest_framework import viewsets, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action

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
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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

    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=401)

        file_uploaded = request.FILES.get('file')
        if not file_uploaded:
            return Response({'detail': 'No file was uploaded.'}, status=400)

        data = request.data.copy()
        data['user'] = user.id
        data['file'] = file_uploaded

        serializer = FileSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_tag(self, request, pk=None):
        file = self.get_object()
        tag_id = request.data.get('tag')
        if tag_id:
            tag, created = Tag.objects.get_or_create(id=tag_id)
            file.tags.add(tag)
            return Response({'status': 'tag added'})
        else:
            return Response({'detail': 'No tag provided.'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_tag(self, request, pk=None):
        file = self.get_object()
        tag_id = request.data.get('tag')
        if tag_id:
            try:
                tag = Tag.objects.get(id=tag_id)
                file.tags.remove(tag)
                return Response({'status': 'tag removed'})
            except Tag.DoesNotExist:
                return Response({'detail': 'Tag not found.'}, status=404)
        else:
            return Response({'detail': 'No tag provided.'}, status=400)

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TagSerializer

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

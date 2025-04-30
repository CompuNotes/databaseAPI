from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework import filters

from .models import File, Tag, Rating
from .serializers import UserSerializer, FileSerializer, TagSerializer, UserDetailSerializer

User = get_user_model()

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class AuthenticatedUserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'tags__name', 'user__username']
    ordering_fields = ['rating']

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
        user = request.user
        if user.is_staff or user.is_superuser or file.user == user:
            tag_id = request.data.get('tag')
            if tag_id:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    file.tags.add(tag)
                    return Response({'status': 'tag added'})
                except Tag.DoesNotExist:
                    return Response({'detail': 'Tag not found.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'detail': 'No tag provided.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def remove_tag(self, request, pk=None):
        file = self.get_object()
        user = request.user
        if user.is_staff or user.is_superuser or file.user == user:
            tag_id = request.data.get('tag')
            if tag_id:
                try:
                    tag = Tag.objects.get(id=tag_id)
                    file.tags.remove(tag)
                    return Response({'status': 'tag removed'})
                except Tag.DoesNotExist:
                    return Response({'detail': 'Tag not found.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'detail': 'No tag provided.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_rating(self, request, pk=None):
        file = self.get_object()
        user = request.user
        rating_value = request.data.get('rating')

        if not rating_value:
            return Response({'detail': 'No rating provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rating_value = int(rating_value)
            if rating_value < 1 or rating_value > 5:
                return Response({'detail': 'Rating must be between 1 and 5.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'detail': 'Invalid rating value.'}, status=status.HTTP_400_BAD_REQUEST)

        rating, created = Rating.objects.update_or_create(
            user_id=user,
            file_id=file,
            defaults={'rating': rating_value}
        )

        if created:
            return Response({'status': 'rating added'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'status': 'rating updated'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated])
    def remove_rating(self, request, pk=None):
        file = self.get_object()
        user = request.user

        try:
            rating = Rating.objects.get(user_id=user, file_id=file)
            if user.is_staff or rating.user_id == user:
                rating.delete()
                return Response({'status': 'rating removed'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        except Rating.DoesNotExist:
            return Response({'detail': 'Rating not found.'}, status=status.HTTP_404_NOT_FOUND)

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

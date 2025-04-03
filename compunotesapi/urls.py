from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, FileViewSet, TagViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'file', FileViewSet, basename='file')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
]
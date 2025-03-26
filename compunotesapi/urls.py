from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, FileViewSet


router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='users')
router.register(r'file', FileViewSet, basename='files')

urlpatterns = [
    path('', include(router.urls)),

]
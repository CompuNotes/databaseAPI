from django.urls import path, include
from rest_framework import routers
from .views import FileViewSet, TagViewSet, UserList, UserDetail
from rest_framework.authtoken.views import obtain_auth_token


router = routers.DefaultRouter()
router.register(r'file', FileViewSet, basename='file')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('', UserList.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('login/', obtain_auth_token, name='api_token_auth'),
]
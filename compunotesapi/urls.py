from django.urls import path, include
from rest_framework import routers
from .views import FileViewSet, TagViewSet, UserList, UserDetail, AuthenticatedUserDetailView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router = routers.DefaultRouter()
router.register(r'file', FileViewSet, basename='file')
router.register(r'tag', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    path('users/', UserList.as_view(), name='user-list'),
    path('<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('me/', AuthenticatedUserDetailView.as_view(), name='authenticated-user-detail'),
    path('login/', TokenObtainPairView.as_view(), name='api_jwt_token_auth'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
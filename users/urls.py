from django.urls import path
from .views import (
    UserAPIView,
    UserDetailApiView,
    ActivateUserApiView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    #path('users/', UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    #path('users/<int:pk>/', UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='user-detail'),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token-verify'),
    path('registro/usuario/', UserAPIView.as_view(), name='cliente-registration'),
    path('activate-user/<uidb64>/<token>', ActivateUserApiView.as_view(), name='activate'),
    
    path('perfil/<str:slug>', UserDetailApiView.as_view(), name='cliente-profile')
]
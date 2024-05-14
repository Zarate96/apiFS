from django.urls import path
from .views import ClienteAPIView

urlpatterns = [
    path('cliente/<str:slug>', ClienteAPIView.as_view(), name='cliente-management'),
]

from django.urls import path
from .views import (RootAPIView, RegisterAPIView)

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('register/', RegisterAPIView.as_view(), name='register'),

]
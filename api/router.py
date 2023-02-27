from rest_framework import routers

from .viewsets.user_viewset import UserViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')

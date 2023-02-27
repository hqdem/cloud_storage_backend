from rest_framework import routers

from .viewsets.user_viewset import UserViewSet
from .viewsets.file_viewset import FileViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'files', FileViewSet, basename='files')

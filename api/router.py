from rest_framework import routers

from .viewsets.user_viewset import UserViewSet
from .viewsets.file_viewset import FileViewSet
from .viewsets.directory_viewset import DirectoryViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'files', FileViewSet, basename='files')
router.register(r'dirs', DirectoryViewSet, basename='dirs')

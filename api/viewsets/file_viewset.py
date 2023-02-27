from rest_framework import viewsets
from rest_framework import permissions

from ..models import File
from ..serializers.file_serializers import FileSerializer
from ..permissions.file_permissions import CheckFileOwnerOnDelete


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckFileOwnerOnDelete]

    def get_queryset(self):
        return File.objects.select_related('owner').all()

    def get_serializer_class(self):
        return FileSerializer

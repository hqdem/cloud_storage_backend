from rest_framework import viewsets
from rest_framework import permissions

from ..models import Directory
from ..serializers.directory_serializers import DirectorySerializer


class DirectoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Directory.objects.select_related('owner').prefetch_related('files', 'files__owner', 'children').all()

    def get_serializer_class(self):
        return DirectorySerializer

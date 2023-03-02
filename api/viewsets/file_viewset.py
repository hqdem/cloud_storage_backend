from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from ..models import File
from ..serializers.file_serializers import FileSerializer, FileCreateSerializer
from ..permissions.file_permissions import CheckFileOwner
from ..filters.file_filters import RootFilesFilter


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CheckFileOwner]
    filter_backends = [RootFilesFilter]

    def get_queryset(self):
        user = self.request.user
        return File.objects.select_related('owner').prefetch_related('shared_users').filter(owner=user)

    def get_serializer_class(self):
        if self.action == 'create':
            return FileCreateSerializer
        return FileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            obj = serializer.save()
            if isinstance(obj, Response):
                return obj
            return Response(FileSerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

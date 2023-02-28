from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from ..models import File
from ..serializers.file_serializers import FileSerializer
from ..permissions.file_permissions import CheckFileOwnerOnDelete


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckFileOwnerOnDelete]

    def get_queryset(self):
        return File.objects.select_related('owner').all()

    def get_serializer_class(self):
        return FileSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            file = serializer.save()
            return Response(FileSerializer(file).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

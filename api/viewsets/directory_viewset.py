from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.response import Response

from ..models import Directory
from ..serializers.directory_serializers import DirectorySerializer, DirectoryCreateSerializer


class DirectoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Directory.objects.select_related('owner').prefetch_related('files', 'files__owner', 'children').all()

    def get_serializer_class(self):
        if self.action == 'create':
            return DirectoryCreateSerializer
        return DirectorySerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        serializer = self.get_serializer(data=data, context={'user': request.user})
        if serializer.is_valid():
            obj = serializer.save()

            if isinstance(obj, Response):
                return obj
            return Response(DirectorySerializer(obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

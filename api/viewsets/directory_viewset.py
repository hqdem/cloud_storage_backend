from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Directory, File
from ..serializers.directory_serializers import DirectorySerializer, DirectoryCreateSerializer
from ..permissions.directory_permissions import CheckDirectoryOwner


class DirectoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CheckDirectoryOwner]

    def get_queryset(self):
        user = self.request.user
        return Directory.objects.select_related('owner', 'parent_dir').prefetch_related('files', 'files__owner', 'children').filter(
            owner=user)

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

    @action(detail=True, methods=['post'])
    def add_files(self, request, pk):
        files = request.FILES.getlist('files')
        owner = request.user
        directory = self.get_object()

        files_obj_list = []
        for file in files:
            files_obj_list.append(File(file=file, owner=owner))
        created_objs = File.objects.bulk_create(files_obj_list)

        directory.files.add(*created_objs)
        return Response(status=status.HTTP_204_NO_CONTENT)

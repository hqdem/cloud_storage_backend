from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Directory, File
from ..serializers.directory_serializers import DirectorySerializer, DirectoryCreateSerializer
from ..permissions.directory_permissions import CheckDirectoryOwner
from ..filters.directory_filters import RootDirectoryFilter
from ..serializers.user_serializers import UserSerializer


class DirectoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CheckDirectoryOwner]
    filter_backends = [RootDirectoryFilter]

    def get_queryset(self):
        user = self.request.user
        queryset = Directory.objects.select_related('owner', 'parent_dir').prefetch_related('files', 'files__owner',
                                                                                            'files__shared_users',
                                                                                            'children',
                                                                                            'shared_users')
        if self.action == 'list':
            return queryset.filter(owner=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return DirectoryCreateSerializer
        elif self.action in ['add_shared_user', 'delete_shared_user']:
            return UserSerializer
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
            files_obj_list.append(File(file=file, owner=owner, directory=directory))
        File.objects.bulk_create(files_obj_list)

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def add_shared_user(self, request, pk):
        data = request.data
        obj = self.get_object()

        user = get_object_or_404(get_user_model(), username=data['username'])
        obj.shared_users.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def delete_shared_user(self, request, pk):
        data = request.data
        obj = self.get_object()

        user = get_object_or_404(get_user_model(), username=data['username'])
        obj.shared_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
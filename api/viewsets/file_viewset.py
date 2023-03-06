from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import File
from ..serializers.file_serializers import FileSerializer, FileCreateSerializer
from ..permissions.file_permissions import CheckFileOwner
from ..filters.file_filters import RootFilesFilter
from ..serializers.user_serializers import UserSerializer


class FileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, CheckFileOwner]
    filter_backends = [RootFilesFilter]

    def get_queryset(self):
        user = self.request.user
        queryset = File.objects.select_related('owner').prefetch_related('shared_users')
        if self.action == 'list':
            return queryset.filter(owner=user)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return FileCreateSerializer
        elif self.action in ['add_shared_user', 'delete_shared_user']:
            return UserSerializer
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

    @action(detail=True, methods=['post'])  # TODO: add implementation of deleting
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

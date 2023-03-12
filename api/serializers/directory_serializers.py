from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from ..models import Directory
from ..serializers.file_serializers import FileSerializer
from ..serializers.user_serializers import UserSerializer


class SubdirectorySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Directory
        fields = [
            'id',
            'name',
            'owner'
        ]


class DirectorySerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    parent_dir = SubdirectorySerializer(read_only=True)
    children_dirs = SubdirectorySerializer(many=True, read_only=True, source='children')
    owner = UserSerializer(read_only=True)
    shared_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Directory
        fields = [
            'id',
            'name',
            'parent_dir',
            'children_dirs',
            'files',
            'owner',
            'shared_users'
        ]


class DirectoryCreateSerializer(serializers.ModelSerializer):
    parent_dir_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Directory
        fields = [
            'name',
            'parent_dir_id'
        ]

    def create(self, validated_data):
        user = self.context.get('user')

        dir_name = validated_data.get('name')
        parent_dir_id = validated_data.get('parent_dir_id', None)

        directory = Directory(name=dir_name, owner=user)

        if parent_dir_id is not None:
            try:
                parent_dir = Directory.objects.get(id=parent_dir_id)
                if user != parent_dir.owner and user not in parent_dir.shared_users.all():
                    return Response({'detail': "Can't create subdirectory. Permission denied"}, status=status.HTTP_403_FORBIDDEN)
                directory.parent_dir = parent_dir
            except ObjectDoesNotExist:
                return Response({'detail': {
                    'parent_dir_id': "Directory with that id doesn't exist"
                }}, status=status.HTTP_400_BAD_REQUEST)

        directory.save()
        return directory

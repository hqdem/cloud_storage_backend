from rest_framework import serializers, status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response

from ..models import Directory
from ..serializers.file_serializers import FileSerializer
from ..serializers.user_serializers import UserSerializer


class SubdirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Directory
        fields = [
            'id',
            'name'
        ]


class DirectorySerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)
    children_dirs = SubdirectorySerializer(many=True, read_only=True, source='children')

    class Meta:
        model = Directory
        fields = [
            'id',
            'name',
            'children_dirs',
            'files',
            'owner'
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
                directory.parent_dir = parent_dir
            except ObjectDoesNotExist:
                return Response({'detail': {
                    'parent_dir_id': "Directory with that id doesn't exist"
                }}, status=status.HTTP_400_BAD_REQUEST)

        directory.save()
        return directory

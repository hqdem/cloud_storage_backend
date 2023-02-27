from rest_framework import serializers

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
    files = FileSerializer(many=True)
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

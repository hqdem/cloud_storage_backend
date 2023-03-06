from rest_framework import serializers, status
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist

from ..models import File, Directory
from ..serializers.user_serializers import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    owner = UserSerializer(read_only=True)
    shared_users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = File
        fields = [
            'id',
            'file',
            'owner',
            'shared_users'
        ]


class FileCreateSerializer(serializers.ModelSerializer):
    parent_dir_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = File
        fields = [
            'file',
            'parent_dir_id'
        ]

    def create(self, validated_data):
        user = self.context.get('user')
        file = validated_data.get('file')
        parent_dir_id = validated_data.get('parent_dir_id', None)

        file = File(file=file, owner=user)

        if parent_dir_id is not None:
            try:
                parent_dir = Directory.objects.get(id=parent_dir_id)
                file.directory = parent_dir
                file.save()
                return file
            except ObjectDoesNotExist:
                return Response({'detail': {
                    'parent_dir_id': "Directory with that id doesn't exist"
                }}, status=status.HTTP_400_BAD_REQUEST)

        file.save()
        return file

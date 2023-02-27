from rest_framework import serializers

from ..models import File
from ..serializers.user_serializers import UserSerializer


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    owner = UserSerializer(read_only=True)

    class Meta:
        model = File
        fields = [
            'id',
            'file',
            'owner'
        ]

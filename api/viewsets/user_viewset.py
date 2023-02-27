from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import mixins

from ..serializers.user_serializers import UserSerializer

user_model = get_user_model()


class UserViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin):
    queryset = user_model.objects.all()

    def get_serializer_class(self):
        return UserSerializer
